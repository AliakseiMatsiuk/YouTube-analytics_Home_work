import os
import json
from googleapiclient.discovery import build
from pprint import pprint


class Channel:
    def __init__(self, channel):
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=channel, part='snippet,statistics').execute()

        self._channel_id = self.channel["items"][0]["id"] # id
        self.title = self.channel['items'][0]['snippet']['title'] # название канала
        self.description = self.channel['items'][0]["snippet"]['description'] # описание канала
        self.url = "https://www.youtube.com/channel/" + self.channel_id # ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']["subscriberCount"] # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount'] # количество видео
        self.views_count = self.channel['items'][0]['statistics']['viewCount'] # общее количество просмотров

    def __str__(self):
        """Возврощает название ютуб канала"""
        return f"Youtube-канал: {self.title}"

    def print_info(self):
        """Выводим информацию о конале"""
        new = json.dumps(self.channel, indent=2, ensure_ascii=False)
        return json.loads(new)

    def to_json(self):
        """Сохраняем информацию по каналу в filename.json"""
        with open("filename.json", "w", encoding="UTF-8") as file:
            data = {"id": self._channel_id,
                    "title": self.title,
                    "description": self.description,
                    "url": self.url,
                    "subscriber_count": self.subscriber_count,
                    "video_count": self.video_count,
                    "views_count": self.views_count}
            json.dump(data, file, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        """Возвращает id канала"""
        return self._channel_id

    @staticmethod
    def get_service():
        """получаем объект для работы с API вне класса"""
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __add__(self, other):
        """Складывает количество подпищиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __lt__(self, other):
        """Сравниквает но < количество подпищиков"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __gt__(self, other):
        """Сравниквает но > количество подпищиков"""
        return int(self.subscriber_count) > int(other.subscriber_count)

class Video: #Создаем класс Video

    def __init__(self, video):
        """Иницеализируем класс по названию, колличеству просмотров и
        колличеству лайков"""
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video = youtube.videos().list(id=video, part='snippet,statistics').execute()
        self.video_title = self.video['items'][0]['snippet']['title']
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __repr__(self):
        """Вывод названия видио"""
        return f"{self.video_title}"

class PLVideo(Video): # Наследуем класс Video в новый класс PLVideo

    def __init__(self, video, playlist):
        """Иницеализируем класс по названию, колличеству просмотров,
            колличеству лайков и названию плейлиста"""
        super().__init__(video)
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = youtube.playlists().list(id=playlist, part='snippet').execute()
        self.playlist_name = self.playlist['items'][0]['snippet']['title']

    def __repr__(self):
        """Вывод названия видио и названия плейлиста"""
        return f"{self.video_title} ({self.playlist_name})"

# channel_id = Channel('UC1eFXmJNkjITxPFWTy6RsWg')    # Редакция
# vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
# pprint(vdud)

# video1 = Video('9lO06Zxhu88')
# video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# print(video1)
# print(video2)



