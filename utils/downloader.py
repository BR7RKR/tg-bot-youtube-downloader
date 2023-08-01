import uuid

from pytube import YouTube


class YouTubeDownloader:

    def download_audio(self, url: str):
        yt = self.get_video_info(url)
        audio_id = uuid.uuid4().fields[-1]
        vid = yt.streams.filter(only_audio=True).first().download("audio", f"{audio_id}.mp3")
        return f'{audio_id}.mp3'

    def get_video_info(self, url: str):
        yt = YouTube(url)
        return yt
