import discord
from discord import app_commands
from localization import get_string
from bot_config import BOT_TOKEN
from utils.load_models import load_model

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Bot
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Import commands
from commands import join, leave, play, pause, resume, queue, skip, nowplaying, chat

# Add commands
commands = [join, leave, play, pause, resume, queue, skip, nowplaying, chat]
for command in commands:
    tree.add_command(command)

@bot.event
async def on_ready():
    print(get_string("BOT_CONNECT_SUCCESS", bot=bot))
    try:
        synced = await tree.sync()
        print(get_string("BOT_COMMAND_SYNC_SUCCESS", len=len(synced)))
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="/play"),
            status=discord.Status.online
        )
        load_model() 
        
    except Exception as e:
        print(get_string("BOT_COMMAND_SYNC_FAIL", error=e))

# 봇 실행
bot.run(BOT_TOKEN)