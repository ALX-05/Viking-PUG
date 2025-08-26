import discord
from discord.app_commands import Range
from discord.enums import ButtonStyle
from discord.ext import commands
import os
from dotenv import load_dotenv

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Get sensitive variables from .env
load_dotenv()

# Log to CLI when bot is logged in
@bot.event
async def on_ready():
    assert bot.user is not None

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# Make queue from players and playercount
def constructQueue(players, playerCount):
    queue = ""
    for i in range(0, playerCount):
        if i < len(players):
            queue = queue + f"{i + 1}: {players[i]} \n"
        else:
            queue = queue + f"{i + 1}: \n"
    return queue

def makeQueueButtons(players, playerCount, pugMessage):
    class QueueButtons(discord.ui.View):
        # Create "Join" button and handle click
        @discord.ui.button(label="join", style=discord.ButtonStyle.success)
        async def playerJoin(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Get discord user who pressed the button
            user = interaction.user
            # Check if player is in queue
            if user in players:
                await interaction.response.send_message(content="You are already in the queue", ephemeral=True)
                return
            # Add player to queue
            players.append(user)
            pugMessage.set_field_at(index=0, name="Queue", value=constructQueue(players, playerCount))
            await interaction.response.edit_message(embed=pugMessage)

        # Create "Leave" button and handle click
        @discord.ui.button(label="leave", style=discord.ButtonStyle.danger)
        async def playerLeave(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Get discord user who pressed the button
            user = interaction.user
            # Check if player is in the queue
            if user not in players:
                await interaction.response.send_message(content="You are not in the queue", ephemeral=True)
                return
            # Remove user from queue
            players.remove(user)
            pugMessage.set_field_at(index=0, name="Queue", value=constructQueue(players, playerCount))
            await interaction.response.edit_message(embed=pugMessage)

    return QueueButtons()


# PUG command
@bot.command(description="Start a PUG queue. Valid arguments are: 1v1, 2v2, 3v3, 4v4")
async def pug(ctx, *args):
    # Check if amount of command arguments is correct
    if len(args) == 0:
        await ctx.send("!pug requires an argument: 1v1, 2v2, 3v3, 4v4")
        return

    if len(args) > 1:
        await ctx.send("!pug only accepts one argument: 1v1, 2v2, 3v3 or 4v4")
        return

    arg = args[0]

    # Handle command argument and check if it is valid
    match arg:
        case "1v1":
            playerCount = 2
            pass
        case "2v2":
            playerCount = 4
            pass
        case "3v3":
            playerCount = 6
            pass
        case "4v4":
            playerCount = 8
            pass
        case _:
            await ctx.send(f"Invalid argument: {arg}. Valid arguments are: 1v1, 2v2, 3v3, 4v4")
            return

    players = []

    # Make queue message
    queue = constructQueue(players, playerCount)
    pugMessage = discord.Embed(title=f"Vikings {arg} PUG", color=0x0060FF)
    pugMessage.add_field(name="Queue", value=queue, inline=False)

    # Add join/leave buttons
    queueButtons = makeQueueButtons(players, playerCount, pugMessage)

    # Send inital queue message
    await ctx.send(embed=pugMessage, view=queueButtons)

# Get discord bot token
botToken = os.getenv("BOT_TOKEN")
if type(botToken) is not str:
    print("ERROR: Couldn't get bot token from .env. Does the file exist and is BOT_TOKEN defined?")
    exit()

bot.run(token=botToken)
