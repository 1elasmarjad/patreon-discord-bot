from bot import CustomBot
from cli_commands.exit import exit_command
from cli_commands.handout import handout_command
from cli_commands.info import info_command
from config import ConfigurationManager

discord_bot = CustomBot()


@discord_bot.event
async def on_ready():
    print(f"Logged in as {discord_bot.user} ({discord_bot.user.id})")

    while True:
        input_data = input("$ ")

        split_data = input_data.split(" ")

        match split_data[0]:
            case "exit":
                return await exit_command(discord_bot, *split_data[1:])

            case "info":
                # patreon info given a discord ID
                await info_command(discord_bot, *split_data[1:])

            case "handout":
                # handout roles to all patrons that are entitled to them and removes roles from those who are not
                await handout_command(discord_bot, *split_data[1:])

            case "help":
                print("TODO: not implemented")

            case _:
                print("Unknown command")


if __name__ == '__main__':
    config = ConfigurationManager().get_config()
    print("Starting bot...")
    discord_bot.run(config["discord_access_token"])
