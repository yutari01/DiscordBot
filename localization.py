# localization.py
import json
import os

translations = {
    "ko": {
        # bot.py
        "BOT_CONNECT_SUCCESS": "{bot.user}가 Discord에 연결되었습니다!",
        "BOT_COMMAND_SYNC_SUCCESS": "{len}개의 명령어가 성공적으로 동기화되었습니다.",
        "BOT_COMMAND_SYNC_FAIL": "명령어 동기화 실패: {error}",
        # commands
        "JOIN_DESCRIPTION": "음성 채널에 참여합니다.",
    },
    "en-US": {
        # bot.py
        "BOT_CONNECT_SUCCESS": "{bot.user} has connected to Discord!",
        "BOT_COMMAND_SYNC_SUCCESS": "{len} commands are successfully synced.",
        "BOT_COMMAND_SYNC_FAIL": "Command sync failed: {error}",
        # commands
        "JOIN_DESCRIPTION": "Join a voice channel.",
    },
    "ja": {
        # bot.py
        "BOT_CONNECT_SUCCESS": "{bot.user}がDiscordに接続しました！",
        "BOT_COMMAND_SYNC_SUCCESS": "{len}のコマンドが正常に同期されました。",
        "BOT_COMMAND_SYNC_FAIL": "コマンドの同期に失敗しました: {error}",
        # commands
        "JOIN_DESCRIPTION": "ボイスチャンネルに参加します。",
    }
}

try:
    from bot_config import BOT_LANGUAGE
    current_language = BOT_LANGUAGE if BOT_LANGUAGE in translations else "en-US"
except (ImportError, AttributeError):
    current_language = "en-US" 
_strings = translations.get(current_language, translations["en-US"])

def get_string(key: str, **kwargs) -> str:
    template = _strings.get(key, key) 
    try:
        return template.format(**kwargs)
    except KeyError as e:
        print(f"Warning: Missing format key {e} for string key '{key}' in language '{current_language}'")
        return template 
    except Exception as e:
        print(f"Error formatting string key '{key}': {e}")
        return template

def get_localized_dict(key: str) -> dict:
    result = {}
    for lang_code, lang_translations in translations.items():
        result[lang_code] = lang_translations.get(key)
    return {k: v for k, v in result.items() if v is not None}