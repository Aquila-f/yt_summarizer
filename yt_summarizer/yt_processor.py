import os
from typing import Optional

from yt_summarizer.models.video_fragment import SceneDetectionInfo, VideoFragment
from yt_summarizer.models.yt_info import Segment, YTInfo
from yt_summarizer.utils.scene_handler import SceneHandler
from yt_summarizer.utils.whisperx_handler import WhisperxHandler
from yt_summarizer.utils.yt_helper import YTHelper

DATA_ROOT = "./data"


class YTProcessor:
    @classmethod
    def get_fragments(cls, yt_url: str) -> Optional[list[VideoFragment]]:
        yt_info = YTHelper.extract_info(yt_url)
        save_dir = os.path.join(DATA_ROOT, yt_info.id)
        subtitle_content = cls.get_subtitle(yt_info)
        scenes_content = cls.get_scenes(save_dir, yt_url)
        fragments = cls.merge_fragments(subtitle_content, scenes_content)
        return fragments

    @staticmethod
    def merge_fragments(
        subtitle_content: list[Segment], scenes_content: list[SceneDetectionInfo]
    ) -> list[VideoFragment]:
        fragment_list = []
        subtitle_idx = 0
        for section in scenes_content:
            sentences = []

            while subtitle_idx < len(subtitle_content):
                subtitle = subtitle_content[subtitle_idx]

                if subtitle.end <= section.start:
                    subtitle_idx += 1
                    continue
                if subtitle.start >= section.end:
                    subtitle_idx -= 1
                    break
                sentences.append(subtitle.text)
                subtitle_idx += 1

            fragment = VideoFragment(**section.model_dump(), sentences=sentences)
            fragment_list.append(fragment)

        return fragment_list

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
    def get_scenes(save_dir: str, yt_url: str) -> Optional[list[SceneDetectionInfo]]:
        try:
            _ = YTHelper.download_video(save_dir, yt_url)
            scenes_content = SceneHandler.detect_scenes(save_dir)
            return scenes_content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
