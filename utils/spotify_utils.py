import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Optional, Dict, Any, Union
from bot_config import CLIENT_ID, CLIENT_SECRET

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_tracks(playlist_id: str) -> List[Dict[str, Any]]:
    """스포티파이 플레이리스트에서 모든 트랙 정보를 가져옵니다."""
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_track_search_query(track: Dict[str, Any]) -> str:
    """스포티파이 트랙 데이터로부터 YouTube 검색 쿼리를 생성합니다."""
    return f"{track['name']} {' '.join([artist['name'] for artist in track['artists']])}"

def spotify_to_youtube_query(spotify_url: str) -> Optional[Union[str, List[str]]]:
    """스포티파이 URL을 유튜브 검색 쿼리로 변환합니다."""
    try:
        if 'track' in spotify_url:
            # 단일 트랙 처리
            track = sp.track(spotify_url)
            return get_track_search_query(track)
        
        elif 'playlist' in spotify_url:
            # 플레이리스트 처리
            playlist_id = spotify_url.split('/')[-1].split('?')[0]
            tracks = get_spotify_tracks(playlist_id)
            youtube_queries = []
            
            for item in tracks:
                track = item['track']
                youtube_queries.append(get_track_search_query(track))
            return youtube_queries
        else:
            raise ValueError("Invalid Spotify URL. Must be a track or playlist URL.")
    
    except Exception as e:
        print(f"Error processing Spotify URL: {e}")
        return None

def get_playlist_info(playlist_url: str) -> Optional[Dict[str, Any]]:
    """스포티파이 플레이리스트 정보를 가져옵니다."""
    try:
        playlist_id = playlist_url.split('/')[-1].split('?')[0]
        return sp.playlist(playlist_id)
    except Exception as e:
        print(f"Error getting playlist info: {e}")
        return None
