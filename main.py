import asyncio

from config import ConfigurationManager
from patreon_api import make_request


async def main():
    config = ConfigurationManager().get_config()

    x = await make_request(f"/campaigns/{config.patreon_campaign_id}", "GET")
    print(x)


if __name__ == '__main__':
    asyncio.run(main())
