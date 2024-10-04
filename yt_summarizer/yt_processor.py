import os
from typing import Optional

from yt_summarizer.models.video_fragment import SceneDetectionInfo
from yt_summarizer.models.yt_info import Segment, YTInfo
from yt_summarizer.utils.scene_handler import SceneHandler
from yt_summarizer.utils.whisperx_handler import WhisperxHandler
from yt_summarizer.utils.yt_helper import YTHelper


class YTProcessor:
    @staticmethod
    def get_subtitle(yt_info: YTInfo) -> Optional[list[Segment]]:
        if yt_info.subtitle is not None:
            subtitle_text = YTHelper.download_subtitle(yt_info.subtitle.url)
            return subtitle_text
        else:
            audio_key = YTHelper.download_audio(yt_info.url)
            audio_text = WhisperxHandler.transcribe(audio_key)

            try:
                os.remove(audio_key)
                print(f"Successfully deleted the file: {audio_key}")
            except OSError as e:
                print(f"Error deleting file {audio_key}: {e.strerror}")

            return audio_text

    @staticmethod
    def get_scenes(yt_url: str) -> Optional[list[SceneDetectionInfo]]:
        try:
            video_key = YTHelper.download_video(yt_url)
            scenes_content = SceneHandler.detect_scenes(video_key)
            return scenes_content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
