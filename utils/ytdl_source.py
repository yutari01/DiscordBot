import discord
import yt_dlp
import asyncio
import time

# yt-dlp 설정
ytdl_format_options = {
    'format': 'bestaudio[abr>192]/bestaudio/best',
    'noplaylist': False,
    'quiet': True,
    'default_search': 'ytsearch',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '192',
    }],
    'ignore_no_formats_error': True,
    'match_filter': '!is_live & live_status!=is_upcoming & availability!=private',
    'retries': 2,
    'extractor_retries': 2,
    'extract_flat': True
}

# ffmpeg 설정
ffmpeg_options = {
    'options': '-vn -b:a 192k',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

# YoutubeDL 인스턴스를 함수 내부로 이동하여 메모리 사용 최적화
# ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')
        self.start_time = time.time()  # 초기화 시 시작 시간 자동 설정

    @classmethod
    async def from_url(cls, url, *, loop=None, download=False):
        loop = loop or asyncio.get_event_loop()
        
        # 함수 내부에서 YoutubeDL 인스턴스 생성 (컨텍스트 매니저 사용)
        def extract_info():
            with yt_dlp.YoutubeDL(ytdl_format_options) as ytdl:
                return ytdl.extract_info(url, download=download)
        
        try:
            data = await loop.run_in_executor(None, lambda: extract_info())
            if 'entries' in data:   # Playlists
                entries = data['entries']
                sources = []
                for entry in entries:
                    filename = entry['url']
                    source = cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=entry)
                    sources.append(source)
                return sources
            
            filename = data['url']
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
            
        except Exception as e:
            raise Exception(f"오디오 추출 중 오류: {str(e)}")
