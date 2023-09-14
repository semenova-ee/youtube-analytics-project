import json
import os
from googleapiclient.discovery import build

from helper.youtube_api_manual import channel_id


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_info(channel_id)
        self._channel_id = channel_id
        self.title = self._data.get('snippet', {}).get('title', '')
        self.description = self._data.get('snippet', {}).get('description', '')
        self.url = f"https://www.youtube.com/channel/{self._channel_id}"
        self.subs = self._data.get('statistics', {}).get('subscriberCount', 0)
        self.video_count = self._data.get('statistics', {}).get('videoCount', 0)
        self.view_count = self._data.get('statistics', {}).get('viewCount', 0)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @staticmethod
    def get_info(channel_id: str) -> dict:
        youtube = Channel.get_service()
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel.get('items', [])[0]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        dict_to_print = self.get_info(channel_id)
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def to_json(self, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self._data, file, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        return self._channel_id

# ulay = Channel('UC4xZXizv7SCrct1j4IIzMzQ')
# ulay.print_info()