from bot import CustomBot
from config import ConfigurationManager
from patreon_api import get_all_pledge_data


async def info_command(discord_bot: CustomBot, *args):
    if len(args) < 1:
        print("Please provide a user discord ID. info <discord_id>")
        return

    discord_id = args[0]

    if not discord_id.isdigit():
        print("Please provide a valid discord ID. info <discord_id>")
        return

    patreon_data = await get_all_pledge_data(ConfigurationManager().get_config()["patreon_campaign_id"])

    for pledge in patreon_data:
        if pledge.discord_id == discord_id:
            print(f"Discord ID: {discord_id}")
            print(f"Email: {pledge.email}")
            print(f"Patron Status: {pledge.patron_status}")
            print(
                f"Entitled Tiers: {', '.join([f"{tier.title} {tier.discord_role_ids}" for tier in pledge.entitled_tiers])}")
            return

    print("No pledge data found for that user. Please make sure the user is a patron.")
