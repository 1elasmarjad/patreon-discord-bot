import aiohttp
from patreon.utils import user_agent_string

from config import ConfigurationManager

_auth_headers = {
    'Authorization': f"Bearer {ConfigurationManager().get_config().patreon_access_token}",
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
