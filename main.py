import asyncio

from config import ConfigurationManager
from patreon_api import make_request


async def main():
    config = ConfigurationManager().get_config()

    params = {
        'page[count]': 20,
        'include': 'user,currently_entitled_tiers',
        'fields[member]': 'patron_status,email',
        'fields[tier]': 'title,discord_role_ids',
    }

    x = await make_request(f"/campaigns/{config.patreon_campaign_id}/members", "GET", params=params)

    for included_data in x['included']:
        if included_data['type'] == 'tier':
            print(included_data['id'], included_data['attributes']['discord_role_ids'])

    #
    # for x in x['data']:
    #     if x['relationships']['currently_entitled_tiers']['data']:
    #         import json
    #         print(json.dumps(x, indent=4))

    import json
    print(json.dumps(x, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
