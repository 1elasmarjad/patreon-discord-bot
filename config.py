import dataclasses
import json
from functools import cache


@dataclasses.dataclass
class ConfigData:
    guild_id: str
    discord_access_token: str
    patreon_access_token: str
    patreon_campaign_id: str


class ConfigurationManager:

    @classmethod
    @cache
    def get_config(cls) -> ConfigData:
        """ Get the configuration data from configurations.json
        :return: the configuration data
        """
        # read configuration.json
        with open('configuration.json') as f:
            config = json.load(f)

            try:
                data = ConfigData(**config)
                cls.__cache = data
                return data
            except TypeError:
                raise ValueError("Invalid configuration file, please check configuration.example.json")
