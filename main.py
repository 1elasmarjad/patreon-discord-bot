from bot import CustomBot
from config import ConfigurationManager

discord_bot = CustomBot()


@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user} ({discord_bot.user.id})")
    # print(len(await get_all_pledge_data(config.patreon_campaign_id)))

    #
    # for x in x['data']:
    #     if x['relationships']['currently_entitled_tiers']['data']:
    #         import json
    #         print(json.dumps(x, indent=4))

    # import json
    # print(json.dumps(x, indent=4))


if __name__ == '__main__':
    config = ConfigurationManager().get_config()
    print("Starting bot...")
    discord_bot.run(config["discord_access_token"])
