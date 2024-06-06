from bot import CustomBot
from config import ConfigurationManager
from patreon_api import get_all_pledge_data

discord_bot = CustomBot()


@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user} ({discord_bot.user.id})")

    while True:
        input_data = input("$ ")

        split_data = input_data.split(" ")

        match split_data[0]:
            case "exit":
                await discord_bot.close()
                exit(0)

            case "info":  # discord info of a user
                if len(split_data) < 2:
                    print("Please provide a user ID")
                    continue

                discord_id = split_data[1]

                patreon_data = await get_all_pledge_data(ConfigurationManager().get_config()["patreon_campaign_id"])

                for pledge in patreon_data:
                    if pledge.discord_id == discord_id:
                        print(f"Discord ID: {discord_id}")
                        print(f"Email: {pledge.email}")
                        print(f"Patron Status: {pledge.patron_status}")
                        print(
                            f"Entitled Tiers: {', '.join([f"{tier.title} {tier.discord_role_ids}" for tier in pledge.entitled_tiers])}")
                        break

            case _:
                print("Unknown command")


if __name__ == '__main__':
    config = ConfigurationManager().get_config()
    print("Starting bot...")
    discord_bot.run(config["discord_access_token"])
