import discord

from config import ConfigurationManager
from patreon_api import CustomPledge, get_all_pledge_data


class CustomBot(discord.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    async def updated_pledge_data() -> list[CustomPledge]:
        config = ConfigurationManager().get_config()
        return await get_all_pledge_data(config["patreon_campaign_id"])
