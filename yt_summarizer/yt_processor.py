import os
from typing import Optional

from yt_summarizer.models.yt_info import Segment, YTInfo
from yt_summarizer.utils.whisperx_handler import WhisperxHandler
from yt_summarizer.utils.yt_helper import YTHelper


class YTProcessor:
    @classmethod
    def get_subtitle(cls, yt_info: YTInfo) -> Optional[list[Segment]]:
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
