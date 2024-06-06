import asyncio

from config import ConfigurationManager
from patreon_api import make_request, get_pledge_data_from_page, get_all_pledge_data


async def main():
    config = ConfigurationManager().get_config()

    print(len(await get_all_pledge_data(config.patreon_campaign_id)))

    #
    # for x in x['data']:
    #     if x['relationships']['currently_entitled_tiers']['data']:
    #         import json
    #         print(json.dumps(x, indent=4))

    # import json
    # print(json.dumps(x, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
