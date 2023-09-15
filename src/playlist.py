from datetime import timedelta

import isodate

from src.video import Video


class PlayList(Video):
    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_playlist_info(playlist_id)
        self._playlist_id = playlist_id
        self.title = self._data.get('items')[0].get('snippet', {}).get('title', '')
        self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"

    @staticmethod
    def get_info_about_videos_in_playlist(playlist_id: str) -> dict:
        youtube = PlayList.get_service()

        playlist_with_videos_response = youtube.playlistItems().list(playlistId=playlist_id,
                                                                     part='contentDetails, snippet',
                                                                     maxResults=50,).execute()
        return playlist_with_videos_response

    @staticmethod
    def get_playlist_info(playlist_id: str) -> dict:
        youtube = PlayList.get_service()

        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()

        return playlist_response

    @property
    def total_duration(self) -> timedelta:
        total_duration_seconds = 0

        # Get the list of videos in the playlist
        playlist_items = self.get_info_about_videos_in_playlist(self._playlist_id)

        # Iterate over each video and sum up their durations
        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_info = self.get_info(video_id)
            video_duration_iso = video_info['contentDetails']['duration']
            video_duration = isodate.parse_duration(video_duration_iso)
            total_duration_seconds += video_duration.total_seconds()
        return timedelta(seconds=total_duration_seconds)

    def show_best_video(self) -> str:
        # Get the list of videos in the playlist
        playlist_items = self.get_info_about_videos_in_playlist(self._playlist_id)

        best_video = None
        max_likes = 0

        # Iterate over each video and find the one with the most likes
        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_info = self.get_info(video_id)
            video_likes = int(video_info['statistics']['likeCount'])

            if video_likes > max_likes:
                max_likes = video_likes
                best_video = video_id

        if best_video:
            return f"https://www.youtube.com/watch?v={best_video}"

        return "No videos found in the playlist."
