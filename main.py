import os
import json
from googleapiclient.discovery import build
#from pprint import pprint


class Channel:
    def __init__(self, channel):
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=channel, part='snippet,statistics').execute()

        self._channel_id = self.channel["items"][0]["id"]
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]["snippet"]['description']
        self.url = "https://www.youtube.com/channel/" + self.channel_id
        self.num_of_sub = self.channel['items'][0]['statistics']["subscriberCount"]
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self):
        """Выводим информацию о конале"""
        new = json.dumps(self.channel, indent=2, ensure_ascii=False)
        return json.loads(new)

    def to_json(self, data):
        """Метод делат запись в json.filename"""
        with open("filename", "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        """Возвращает id канала"""
        return self._channel_id

    @staticmethod
    def get_service():
        """получаем объект для работы с еAPI вне класса"""
        api_key: str = os.getenv('AFI_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

#vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')





