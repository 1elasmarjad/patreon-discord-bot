import discord
from discord.utils import find

from config import ConfigurationManager
from patreon_api import CustomPledge, get_all_pledge_data


class CustomBot(discord.Bot):

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True  # noqa

        super().__init__(*args, **kwargs, intents=intents)

    @staticmethod
    async def get_members_with_role(role_id: int, guild: discord.Guild) -> list[discord.Member]:
        role: discord.Role = find(lambda r: r.id == role_id, guild.roles)
        return [member for member in guild.members if role in member.roles]

    @staticmethod
    async def updated_pledge_data() -> list[CustomPledge]:
        config = ConfigurationManager().get_config()
        return await get_all_pledge_data(config["patreon_campaign_id"])
