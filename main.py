import os
import json
from googleapiclient.discovery import build
from pprint import pprint
import isodate
import datetime


class Channel:
    def __init__(self, channel):
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=channel, part='snippet,statistics').execute()

        self._channel_id = self.channel["items"][0]["id"]  # id
        self.title = self.channel['items'][0]['snippet']['title']  # название канала
        self.description = self.channel['items'][0]["snippet"]['description']  # описание канала
        self.url = "https://www.youtube.com/channel/" + self.channel_id  # ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']["subscriberCount"]  # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']  # количество видео
        self.views_count = self.channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

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


class Video:  # Создаем класс Video

    def __init__(self, video):
        """Иницеализируем класс по названию, колличеству просмотров и
        колличеству лайков"""
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        try:
            self.video = youtube.videos().list(id=video, part='snippet,statistics').execute()
            self.video_id = self.video['items'][0]['id']
            self.video_title = self.video['items'][0]['snippet']['title']
            self.view_count = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except:
            self.video_id = video
            self.video_title = None
            self.view_count = None
            self.like_count = None

    def __repr__(self):
        """Вывод названия видио"""
        return f"{self.video_title}"


class PLVideo(Video):  # Наследуем класс Video в новый класс PLVideo

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


class Mixin:  # класс Mixin в помощь остальным
    def __init__(self, playlist_id):
        """Инициализаторы плейсилстов и видио"""
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                            maxResults=50, ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()


class PlayList(Mixin):
    def __init__(self, playlist_id):
        super().__init__(playlist_id)
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id

    @property
    def total_duration(self):
        """Подсчёт сцммарной длительности плейслиста"""
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста
        (по количеству лайков)"""
        count = [1]
        id = ""
        for i in self.video_response["items"]:
            if int(i['statistics']['likeCount']) > count[0]:
                count[0] = int(i['statistics']['likeCount'])
                id = i["id"]
        return f'https://youtu.be/{id}'


# video1 = Video('9lO06Zxhu88')
# broken_video = Video('broken_video_id')
# print(broken_video.video_id)
