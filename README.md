# Discord Music Bot

간단하면서도 강력한 디스코드 뮤직봇입니다. `discord.py` 라이브러리를 사용하여 제작되었으며, 명령어를 통해 디스코드 음성 채널에서 유튜브, 스포티파이 등 다양한 소스의 음악을 재생하고 제어할 수 있습니다.
![MusicBot Sample Image](https://cdn.discordapp.com/attachments/1082144833826738270/1360158046717743154/image.png?ex=67fa1964&is=67f8c7e4&hm=3d34e1130fdcbc2cfb770c4d61b40f79b615be0b9a604124f5c2e8b071f67927&)
## ✨ 주요 기능
* **다양한 소스 지원**: 유튜브 URL, 검색어 및 Spotify 트랙/재생목록 재생을 지원합니다.
* **슬래시 명령어**: 모든 기능을 사용하기 쉬운 슬래시 명령어로 제공합니다.
* **버튼 지원**: 버튼 GUI로 간편하게 이용할 수 있습니다.
* **다국어 지원**: 디스코드의 언어 설정에 따라 봇의 언어가 바뀝니다.(개발중)

## ⚙️ 사전 준비
* **Python**: Python 3.12 이상 버전 설치
* **Discord 계정**: 디스코드 계정 및 봇을 추가할 서버 (관리자 권한 필요)
* **Discord Bot Application**:
    * [Discord Developer Portal](https://discord.com/developers/applications)에서 봇 애플리케이션 생성
    * 생성된 봇의 **Token** 복사
    * Bot 섹션에서 필요한 **Privileged Gateway Intents** 활성화
* **Youtube API Keys**: 유튜브에서 썸네일을 불러오고 공식 음원임을 확인하기 위해 API를 사용합니다. 
* **Spotify API Keys**: Spotify 재생 기능을 온전히 사용하려면 Spotify Developer Dashboard에서 앱을 등록하고 Client ID와 Client Secret을 발급받아야 할 수 있습니다.


## 🚀 설치 및 실행 방법

1.  **저장소 복제:**
    ```bash
    git clone https://github.com/yutari01/MusicBot.git
    cd MusicBot
    ```

2.  **필요 라이브러리 설치:**

    * **방법 1: 설치 스크립트 사용 (Linux/macOS)**
        * `install.sh` 스크립트에 실행 권한을 주고 실행합니다. 
        ```bash
        chmod +x install.sh
        ./install.sh
        ```
    * **방법 2: 수동 설치 (모든 환경)**
        * 음악 재생 및 기능 구현에 필요한 라이브러리들을 수동으로 설치합니다.

3.  **설정 파일 생성:**
    * `bot_sample_config.py` 파일을 복사하여 `bot_config.py` 파일을 생성합니다.
    ```bash
    cp bot_sample_config.py bot_config.py
    ```
    * 생성된 `bot_config.py` 파일을 열어 필요한 정보를 입력합니다. 
    ```python
    # bot_config.py (예시)
    BOT_TOKEN       = 'Your Discord Token Here'
    YT_TOKEN        = 'Your YouTube Token Here'
    CLIENT_ID       = 'Your Spotify Client ID Here'
    CLIENT_SECRET   = 'Your Spotify Client Secret Here'
    BOT_LANGUAGE    = 'en'    # ko = 한국어, en-US = English, ja = 日本語
    ```
4.  **봇 실행:**

    * **방법 1: 실행 스크립트 사용 (Linux/macOS)**
        * `start.sh` 스크립트에 실행 권한을 주고 실행합니다.
        ```bash
        chmod +x start.sh
        ./start.sh
        ```
    * **방법 2: 직접 실행 (모든 환경)**
        ```bash
        python bot.py
        ```
    * 콘솔에 봇 연결 및 커맨드 동기화 성공 메시지가 나타나면 정상적으로 실행된 것입니다.

## 🤖 명령어 
* 봇이 온라인 상태가 되면, 디스코드 채팅창에 `/`를 입력하여 사용 가능한 슬래시 명령어를 확인하고 사용할 수 있습니다.
* **주요 명령어**
      * `/join`: 봇을 음성 채널에 들어오게 합니다.
      * `/leave`: 봇을 음성 채널에서 내보냅니다.
      * `/nowplaing`: 현재 재생 중인 곡 정보를 확인합니다.
      * `/pause`: 현재 재생 중인 음악을 일시정지합니다.
      * `/play`: YouTube, Spotify의 URL, 검색어 또는 플레이리스트를 재생합니다.
      * `/queue`: 현재 대기열을 확인합니다.
      * `/resume`: 일시정지된 음악을 이어서 재생합니다.
      * `/skip`: 현재 재생 중인 곡을 건너뛰고 다음 곡을 재생합니다.