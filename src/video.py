import json
import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key = os.getenv("YOUTUBE_API_KEY")

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_info(video_id)
        self._video_id = video_id
        self.title = self._data.get('snippet', {}).get('title', '')
        self.url = f"https://www.youtube.com/watch?v={self._video_id}"
        self.like_count = self._data.get('statistics', {}).get('likeCount', 0)
        self.view_count = self._data.get('statistics', {}).get('viewCount', 0)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @staticmethod
    def get_info(video_id: str) -> dict:
        youtube = Video.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        return video_response.get('items', [])[0]

    def __str__(self):
        return self.title

class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.plalist_id = playlist_id
