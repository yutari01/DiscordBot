import discord
import asyncio
import yt_dlp as ytdl
import re
from discord import app_commands, Embed
from collections import deque
from typing import Optional, Tuple, List

from utils import ytdl_source
from utils.play_next import play_next
from utils.queues import queues
from utils.spotify_utils import spotify_to_youtube_query, get_playlist_info

# Initialize YouTube downloader
ytdl = ytdl.YoutubeDL(ytdl_source.ytdl_format_options)

class SourceType:
    """음악 소스 유형을 정의하는 클래스"""
    YOUTUBE_URL = "youtube_url"
    YOUTUBE_PLAYLIST = "youtube_playlist"
    SPOTIFY_TRACK = "spotify_track"
    SPOTIFY_PLAYLIST = "spotify_playlist"
    SEARCH_QUERY = "search_query"

def determine_source_type(query: str) -> Tuple[str, str]:
    """사용자 입력에서 음악 소스 유형을 판별합니다."""
    if "https://open.spotify.com/playlist/" in query:
        return SourceType.SPOTIFY_PLAYLIST, query
        
    elif "https://open.spotify.com/track/" in query:
        search_query = spotify_to_youtube_query(query)
        if search_query:
            return SourceType.SPOTIFY_TRACK, f"ytsearch:{search_query}"
        return SourceType.SPOTIFY_TRACK, None
        
    elif "playlist?list=" in query:
        return SourceType.YOUTUBE_PLAYLIST, query
        
    elif "&list=" in query:
        match = re.search(r"watch\?v=([a-zA-Z0-9_-]+)&list=([a-zA-Z0-9_-]+)", query)
        if match:
            return SourceType.YOUTUBE_PLAYLIST, f"https://www.youtube.com/playlist?list={match.group(2)}"
        return SourceType.YOUTUBE_URL, query
        
    elif "http" in query or "www." in query:
        return SourceType.YOUTUBE_URL, query
        
    else:
        return SourceType.SEARCH_QUERY, f"ytsearch:{query}"

@app_commands.command(name="play", description="YouTube, Spotify의 URL, 검색어 또는 플레이리스트를 재생합니다.")
@app_commands.describe(search="재생할 YouTube, Spotify의 URL, 검색어 또는 플레이리스트 URL (예: '아이유 좋은날' 또는 'https://www.youtube.com/playlist?...')")
async def play(interaction: discord.Interaction, search: str):
    try:
        # 사용자가 음성 채널에 있는지 확인
        if not interaction.user.voice:
            await interaction.response.send_message("먼저 음성 채널에 들어가야 합니다!", ephemeral=True)
            return

        # 음성 채널에 연결되어 있지 않다면 연결
        if not interaction.guild.voice_client:
            channel = interaction.user.voice.channel
            await channel.connect()

        voice_client = interaction.guild.voice_client
        guild_id = interaction.guild.id

        # 큐가 없으면 초기화
        if guild_id not in queues:
            queues[guild_id] = deque()

        await interaction.response.defer()

        # 소스 유형 판별 및 처리
        source_type, processed_input = determine_source_type(search)
        
        if source_type == SourceType.SPOTIFY_TRACK and processed_input is None:
            await interaction.followup.send("유효하지 않은 Spotify 트랙 URL입니다.")
            return
        
        # 각 소스 유형별 처리
        if source_type == SourceType.SPOTIFY_PLAYLIST:
            await handle_spotify_playlist(interaction, search, guild_id, voice_client)
            
        elif source_type in [SourceType.SPOTIFY_TRACK, SourceType.YOUTUBE_URL, SourceType.SEARCH_QUERY]:
            await handle_single_track(interaction, processed_input, source_type, guild_id, voice_client)
            
        elif source_type == SourceType.YOUTUBE_PLAYLIST:
            await handle_youtube_playlist(interaction, processed_input, guild_id, voice_client)

        # 재생 중이 아니면 재생 시작
        if not voice_client.is_playing():
            await play_next(interaction.guild, interaction.channel, interaction.user.id)

    except Exception as e:
        await interaction.followup.send(f"재생 중 오류 발생: {str(e)}")

async def handle_spotify_playlist(interaction: discord.Interaction, spotify_url: str, guild_id: int, voice_client: discord.VoiceClient):
    """스포티파이 플레이리스트 URL을 처리합니다."""
    queries = spotify_to_youtube_query(spotify_url)
    if queries is None:
        await interaction.followup.send("유효하지 않은 URL이거나 스포티파이에서 자동 생성된 플레이이스트의 경우 지원하지 않습니다.")
        return
    
    count = 0
    loop = asyncio.get_event_loop()
    
    for query in queries:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{query}", download=False))
        for entry in data['entries']:
            if entry:
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                queues[guild_id].append(video_url)
                count += 1

        if not voice_client.is_playing():
            await play_next(interaction.guild, interaction.channel, interaction.user.id)
    
    playlist_info = get_playlist_info(spotify_url)
    playlist_name = playlist_info.get('name', 'Spotify Playlist') if playlist_info else 'Spotify Playlist'
    
    embed = Embed(
        title="🎵 Added Spotify Playlist to Queue", 
        description=f"{count}곡이 재생목록에 추가되었습니다.", 
        color=discord.Color.green()
    )
    embed.add_field(name="Playlist", value=playlist_name, inline=False)
    await interaction.followup.send(embed=embed)

async def handle_youtube_playlist(interaction: discord.Interaction, playlist_url: str, guild_id: int, voice_client: discord.VoiceClient):
    """YouTube 플레이리스트 URL을 처리합니다."""
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(playlist_url, download=False))
    
    success_count = 0
    fail_count = 0
    first_song_title = None
    
    if 'entries' in data:
        for entry in data['entries']:
            if entry:
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                video_title = entry.get('title', '제목 없음')
                
                if video_title != '[Private video]':
                    if first_song_title is None:
                        first_song_title = video_title
                    queues[guild_id].append(video_url)
                    success_count += 1
                else:
                    fail_count += 1
                    
            if not voice_client.is_playing():
                await play_next(interaction.guild, interaction.channel, interaction.user.id)

    embed = Embed(
        title="🎵 Added Youtube Playlist to Queue", 
        description=f"{success_count}곡이 재생목록에 추가되었습니다.", 
        color=discord.Color.pink()
    )
    
    if first_song_title:
        embed.add_field(name="첫 번째 곡", value=first_song_title, inline=False)
        
    if fail_count > 0:
        embed.set_footer(text=f"{fail_count}곡을 추가하지 못했습니다.")
        
    if 'title' in data and data['title']:
        embed.add_field(name="플레이리스트 제목", value=data['title'], inline=False)
        
    await interaction.followup.send(embed=embed)

async def handle_single_track(interaction: discord.Interaction, input_query: str, source_type: str, guild_id: int, voice_client: discord.VoiceClient):
    """단일 트랙 (URL 또는 검색)을 처리합니다."""
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(input_query, download=False))

    if source_type == SourceType.SEARCH_QUERY or source_type == SourceType.SPOTIFY_TRACK:
        for entry in data['entries']:
            if entry:
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                queues[guild_id].append(video_url)
            
                embed = Embed(
                    title="🎵 Added Music to Queue", 
                    description=f"🔍 {entry.get('title', '정보 없음')}", 
                    color=discord.Color.purple()
                )
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("입력한 검색어로 곡을 찾을 수 없습니다.")
            
    else:  # URL type
        if not data.get('id'):
            await interaction.followup.send("입력한 URL로 곡을 찾을 수 없습니다.")
            return
            
        song = f"https://www.youtube.com/watch?v={data['id']}"
        queues[guild_id].append(song)
        
        embed = Embed(
            title="🎵 곡이 큐에 추가되었습니다", 
            description=f"🔍 {data.get('title', '정보 없음')}", 
            color=discord.Color.pink()
        )
        await interaction.followup.send(embed=embed)
