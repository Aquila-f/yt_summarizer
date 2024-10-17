import os
from typing import Optional

from yt_summarizer.models.video_fragment import SceneExtractInfo, VideoFragment
from yt_summarizer.models.yt_info import Segment, YTInfo
from yt_summarizer.service.scene_handler import SceneHandler
from yt_summarizer.service.whisperx_handler import WhisperxHandler
from yt_summarizer.service.yt_helper import YTHelper
from yt_summarizer.utils.file_operation import save_list

DATA_ROOT = "./savedata"


class YTProcessor:
    @staticmethod
    def merge_same_key(
        fragments: list[VideoFragment],
    ) -> list[VideoFragment]:
        fragment_dict: dict[str, VideoFragment] = {}
        for fragment in fragments:
            if fragment.key in fragment_dict:
                fragment_dict[fragment.key].sentences.extend(fragment.sentences)
                if fragment.has_chart:
                    fragment_dict[fragment.key].img_path = fragment.img_path
                    fragment_dict[fragment.key].img_timestamp = fragment.img_timestamp
                    fragment_dict[fragment.key].has_chart = True
            else:
                fragment_dict[fragment.key] = fragment
        return [fragment for fragment in fragment_dict.values()]

    @staticmethod
    def merge_fragments(
        subtitle_content: list[Segment], scenes_content: list[SceneExtractInfo]
    ) -> list[VideoFragment]:
        fragment_list = []
        subtitle_idx = 0
        for section in scenes_content:
            sentences = []

            while subtitle_idx < len(subtitle_content):
                subtitle = subtitle_content[subtitle_idx]

                if subtitle.end <= section.start:
                    subtitle_idx += 1
                elif subtitle.end <= section.end:
                    sentences.append(subtitle.text)
                    subtitle_idx += 1
                else:
                    if (section.end - subtitle.start) > (subtitle.end - section.end):
                        sentences.append(subtitle.text)
                        subtitle_idx += 1
                    break

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
    def get_scenes(save_dir: str, yt_url: str) -> list[SceneExtractInfo]:
        YTHelper.download_video(save_dir, yt_url)
        scenes_content = SceneHandler.extract_scenes(save_dir)
        return scenes_content

    @classmethod
    def get_topics(cls, yt_url: str) -> Optional[list[VideoFragment]]:
        yt_info = YTHelper.extract_info(yt_url)
        save_dir = os.path.join(DATA_ROOT, yt_info.id)
        subtitle_content = cls.get_subtitle(yt_info)
        scenes_content = cls.get_scenes(save_dir, yt_url)
        fragments = cls.merge_fragments(subtitle_content, scenes_content)
        topics = cls.merge_same_key(fragments)
        save_list(topics, os.path.join(save_dir, "topics.json"))
        return fragments
