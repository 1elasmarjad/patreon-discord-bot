import dataclasses
import json
from typing import TypedDict


@dataclasses.dataclass
class ConfigData:
    guild_id: str
    discord_access_token: str
    patreon_access_token: str
    patreon_campaign_id: str


class ConfigurationManager:

    @classmethod
    def get_config(cls) -> ConfigData:
        # read configuration.json
        with open('configuration.json') as f:
            config = json.load(f)

            try:
                return ConfigData(**config)
            except TypeError:
                raise ValueError("Invalid configuration file, please check configuration.example.json")
