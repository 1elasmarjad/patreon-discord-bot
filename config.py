import json
from functools import cache
from typing import Optional, TypedDict

from discord.abc import Snowflake


class AlwaysGiveRole(TypedDict):
    discord_user_id: Snowflake
    discord_role_id: str


class ConfigData(TypedDict):
    guild_id: str
    discord_access_token: str
    patreon_access_token: str
    patreon_campaign_id: str
    always_give_roles: Optional[list[AlwaysGiveRole]]


class ConfigurationManager:
    __cache: Optional[ConfigData] = None

    @classmethod
    @cache
    def get_config(cls) -> ConfigData:
        """ Get the configuration data from configurations.json
        :return: the configuration data
        """
        # read configuration.json
        with open('configuration.json') as f:
            if cls.__cache:
                return cls.__cache

            config = json.load(f)
            cls.__cache = config
            return config
