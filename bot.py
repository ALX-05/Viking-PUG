import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    assert bot.user is not None

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


# Test command
@bot.command(description="Test the bot is working properly")
async def test(ctx):
    await ctx.send("Hello world!")


# PUG command
@bot.command(description="Start a PUG queue. Valid arguments are: 1v1, 2v2, 3v3, 4v4")
async def pug(ctx, *args):
    if len(args) == 0:
        await ctx.send("Argument required. Valid arguments are: 1v1, 2v2, 3v3, 4v4")
        return

    if len(args) > 1:
        await ctx.send("!pug only accepts one argument: 1v1, 2v2, 3v3 or 4v4")
        return

    arg = args[0]

    match arg:
        case "1v1":
            pass
        case "2v2":
            pass
        case "3v3":
            pass
        case "4v4":
            pass
        case _:
            await ctx.send(
                f"Invalid argument: {arg}. Valid arguments are: 1v1, 2v2, 3v3, 4v4"
            )
            return

    await ctx.send(f"PUG {arg}")


load_dotenv()
botToken = os.getenv("BOT_TOKEN")
if type(botToken) is not str:
    print(
        "ERROR: Couldn't get bot token from .env. Does the file exist and BOT_TOKEN is defined?"
    )
    exit()
bot.run(token=botToken)
