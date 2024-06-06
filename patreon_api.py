import dataclasses
from typing import Literal, TypedDict

import aiohttp
from discord.abc import Snowflake
from patreon.utils import user_agent_string

from config import ConfigurationManager

_auth_headers = {
    'Authorization': f"Bearer {ConfigurationManager().get_config()["patreon_access_token"]}",
    'User-Agent': user_agent_string()
}


class PatreonAPIError(Exception):
    pass


async def make_request(path: str, meth: str, params: dict = None, headers: dict = None,
                       data: dict = None, json: dict = None, **kwargs) -> dict:
    async with aiohttp.ClientSession() as session:
        if path.startswith('/'):
            path = path[1:]

        url = f"https://www.patreon.com/api/oauth2/v2/{path}"

        if not headers:
            headers = {}

        headers.update(_auth_headers)

        response = await session.request(
            meth,
            url,
            params=params,
            headers=headers,
            data=data,
            json=json,
            **kwargs
        )

        if response.status != 200:
            raise PatreonAPIError(f"Error making request to Patreon API: {response.status}")

        return await response.json()


@dataclasses.dataclass
class CustomTier:
    id: str
    title: str
    discord_role_ids: list[Snowflake]


@dataclasses.dataclass
class CustomPledge:
    id: str
    discord_id: Snowflake
    email: str
    patron_status: Literal['declined_patron'] | Literal['active_patron'] | Literal['former_patron'] | None
    entitled_tiers: list[CustomTier]


class PatreonPledgesResponse(TypedDict):
    data: list[dict]
    included: list[dict]


async def get_all_pledge_data(campaign_id: str | int, per_page: int = 500) -> list[CustomPledge]:
    """ Gets all pledge data from a Patreon campaign
    :param campaign_id: the ID of the campaign
    :param per_page: the number of pledges to get per page,
    :return: a list of Custom
    """
    if per_page > 500 or per_page < 1:
        raise ValueError("per_page must be between 1 and 500")  # according to the Patreon API docs

    params = {
        'page[count]': per_page,
        'include': 'user,currently_entitled_tiers',
        'fields[member]': 'patron_status,email',
        'fields[tier]': 'title,discord_role_ids',
        'fields[user]': 'social_connections',
    }

    # initial request
    patreon_resp = await make_request(f"/campaigns/{campaign_id}/members", "GET", params=params)

    pledge_data = await get_pledge_data_from_page(patreon_resp)  # get all the pledges from the initial page
    while next_page := patreon_resp.get("links", {}).get("next"):
        patreon_resp = await make_request(next_page, "GET", params=params)
        pledge_data.extend(await get_pledge_data_from_page(patreon_resp))

    return pledge_data


async def get_pledge_data_from_page(resp_json: PatreonPledgesResponse) -> list[CustomPledge]:
    """ Given one pagination page of Patreon pledges, return a list of CustomPledge objects
    :param resp_json: The JSON response from the Patreon API
    :return: A list of CustomPledge objects
    """
    tier_id_to_discord_roles: dict[str, CustomTier] = {}  # tier_id: CustomTier
    patreon_id_to_discord_id: dict[str, Snowflake] = {}  # patreon_id: discord_id

    for inc_data in resp_json["included"]:
        if inc_data["type"] == "tier":
            tier_id = inc_data["id"]

            tier_id_to_discord_roles[tier_id] = CustomTier(
                id=tier_id,
                title=inc_data.get("attributes", {}).get("title", ""),
                discord_role_ids=inc_data.get("attributes", {}).get("discord_role_ids", [])
            )

        elif inc_data["type"] == "user":
            patreon_id = inc_data["id"]

            _social = inc_data['attributes'].get('social_connections')
            if not _social:
                continue

            _disc = _social.get('discord', None)
            if not _disc:
                continue

            if not (discord_id := _disc.get('user_id', None)):
                continue

            if discord_id:
                patreon_id_to_discord_id[patreon_id] = discord_id

    pledge_data: list[CustomPledge] = []

    for usr_data in resp_json["data"]:
        entitled_tiers: list[dict] = usr_data["relationships"]["currently_entitled_tiers"]["data"]

        pledge = CustomPledge(
            id=usr_data["id"],
            discord_id=patreon_id_to_discord_id.get(usr_data["relationships"]["user"]["data"]["id"]),
            email=usr_data["attributes"]["email"],
            patron_status=usr_data["attributes"]["patron_status"],
            entitled_tiers=[]
        )

        for tier in entitled_tiers:
            tier_id = tier["id"]
            tier_data = tier_id_to_discord_roles.get(tier_id)

            if not tier_data:
                continue

            pledge.entitled_tiers.append(tier_data)

        pledge_data.append(pledge)

    return pledge_data
