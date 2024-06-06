from bot import CustomBot


async def exit_command(discord_bot: CustomBot, *args):
    await discord_bot.close()
    exit(0)
