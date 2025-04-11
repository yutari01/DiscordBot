import discord
import time

from discord import app_commands
from utils.ytdl_source import YTDLSource
from googleapiclient.discovery import build
from bot_config import YT_TOKEN

@app_commands.command(name="nowplaying", description="현재 재생 중인 곡 정보를 확인합니다.")
async def nowplaying(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        await interaction.response.send_message("현재 재생 중인 음악이 없습니다.", ephemeral=True)
        return

    player = voice_client.source
    if not isinstance(player, YTDLSource):
        await interaction.response.send_message("현재 재생 중인 곡 정보를 가져올 수 없습니다.", ephemeral=True)
        return

    try:
        embed = await create_nowplaying_embed(interaction, player)
        await interaction.response.send_message(embed=embed)
        
    except Exception as e:
        await interaction.response.send_message(f"현재 재생 정보 확인 중 오류: {str(e)}", ephemeral=True)

async def create_nowplaying_embed(interaction: discord.Interaction, player: YTDLSource):
    youtube = build('youtube', 'v3', developerKey=YT_TOKEN)
    
    channel_id = player.data.get('channel_id')
    if not channel_id:
        raise ValueError("채널 ID를 찾을 수 없습니다.")

    channel_response = youtube.channels().list(part="snippet", id=channel_id).execute()
    uploader_thumbnail = channel_response['items'][0]['snippet']['thumbnails']['default']['url'] if 'items' in channel_response else None

    embed = discord.Embed(title=player.title, url=f"https://www.youtube.com/watch?v={player.data.get('id')}", color=0x00ff00)
    
    uploader_name = player.data.get('uploader', 'Unknown Uploader')
    channel_url = f"https://www.youtube.com/channel/{channel_id}"
    embed.set_author(name=uploader_name, url=channel_url, icon_url=uploader_thumbnail or player.data.get('thumbnail'))

    if player.data.get('thumbnail'):
        embed.set_thumbnail(url=player.data.get('thumbnail'))

    duration_str = format_duration(player.data.get('duration', 0))
    embed.add_field(name="Duration", value=duration_str, inline=True)
    embed.add_field(name="Request", value=interaction.user.mention, inline=True)

    if player.start_time:
        remaining_str = format_duration(max(0, player.data.get('duration', 0) - (time.time() - player.start_time)))
        embed.add_field(name="Remaining", value=remaining_str, inline=True)
    else:
        embed.add_field(name="Remaining", value="시간 정보 없음", inline=True)

    voice_channel_name = interaction.guild.voice_client.channel.name if interaction.guild.voice_client else "Unknown Channel"
    embed.set_footer(text=f"{voice_channel_name} / {interaction.client.user.name}")

    return embed

def format_duration(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"