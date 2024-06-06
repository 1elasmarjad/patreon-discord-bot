from typing import Optional

import discord
from discord.utils import find

from bot import CustomBot
from config import ConfigurationManager, AlwaysGiveRole
from patreon_api import get_patreon_tiers


async def handout_command(discord_bot: CustomBot, *args: str):
    config = ConfigurationManager().get_config()

    forced_roles: Optional[list[AlwaysGiveRole]] = config["always_give_roles"]

    guild: discord.Guild = discord_bot.get_guild(int(config["guild_id"]))

    # --- handout forced roles ---
    for role in forced_roles:
        role_obj: discord.Role = find(lambda r: r.id == int(role["discord_role_id"]), guild.roles)

        if not role_obj:
            print(
                f"IGNORING ERROR: Role with ID {role['discord_role_id']} "
                f"not found for forced role user {role['discord_user_id']}"
            )
            continue

        user_id = role["discord_user_id"]
        member = guild.get_member(int(user_id))

        try:
            await member.add_roles(role_obj)
        except discord.Forbidden:
            print(f"IGNORING ERROR: Bot does not have permissions to add roles to {member}")
        except discord.HTTPException as e:
            print(f"IGNORING ERROR: {e}")

    # --- get all discord ids of patreon perks ---
    all_tiers = await get_patreon_tiers(config["patreon_campaign_id"])

    all_patreon_discord_role_ids = set()
    for tier in all_tiers:
        if tier.discord_role_ids is None:
            continue
        all_patreon_discord_role_ids.update([x for x in tier.discord_role_ids if x is not None])

    # --- remove roles if they are not entitled ---
    members_with_outdated_patreon_roles: set[discord.Member] = set()
    for tier in all_tiers:
        if tier.discord_role_ids is not None:
            for role_id in tier.discord_role_ids:
                members = await discord_bot.get_members_with_role(int(str(role_id)), guild)
                members_with_outdated_patreon_roles.update(members)

    raise NotImplementedError("TODO")

    for member in members_with_outdated_patreon_roles:
        pass

    # go through people that currently have roles and remove them if they are not entitled TODO
    # patron_data: list[CustomPledge] = await get_all_pledge_data(config["patreon_campaign_id"])
