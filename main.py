import os
import json

from googleapiclient.discovery import build


class YouTobe:

    def __init__(self, channel_id):
        self.channel_id = channel_id
        # API_KEY скопирован из гугла и вставлен в переменные окружения
        api_key: str = os.getenv('API_KEY')
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()


    def print_info(self):
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

# channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь

youtube = YouTobe("UCMCgOm8GZkHp8zJ6l7_hIuA")
youtube.print_info()







