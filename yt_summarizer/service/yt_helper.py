import json
import os
import random
import string
from typing import Optional

import requests
import yt_dlp

from yt_summarizer.models.yt_info import Segment, SubtitleUrl, YTInfo

yt_info_extractor_opts = {
    "writesubtitles": True,
    "subtitleslangs": ["all"],
    "skip_download": True,
}

yt_audio_extractor_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }
    ],
    "outtmpl": "-",
    "logtostderr": True,
}

yt_video_extractor_opts = {
    "format": "bestvideo/best",
    "merge_output_format": "mp4",
    "postprocessors": [
        {
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }
    ],
    "outtmpl": "-",
}


class YTHelper:
    @staticmethod
    def extract_info(yt_url: str) -> Optional[YTInfo]:
        try:
            with yt_dlp.YoutubeDL(yt_info_extractor_opts) as ydl:
                info_dict = ydl.extract_info(yt_url, download=False)
                subtitles = info_dict.get("subtitles", {})

                tmp_subinfo = None
                for key in ["zh", "en"]:
                    if key in subtitles:
                        tmp_subinfo = SubtitleUrl(
                            lang=key,
                            ext=subtitles[key][0]["ext"],
                            url=subtitles[key][0]["url"],
                            name=subtitles[key][0]["name"],
                        )
                        break

                return YTInfo(
                    url=yt_url,
                    id=info_dict["id"],
                    title=info_dict["title"],
                    length=info_dict["duration"],
                    author=info_dict["uploader"],
                    channel_url=info_dict["channel_url"],
                    thumbnail_url=info_dict["thumbnail"],
                    views=info_dict["view_count"],
                    subtitle=tmp_subinfo,
                )
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def download_audio(yt_url: str) -> Optional[str]:
        save_key = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        yt_audio_extractor_opts["outtmpl"] = f"{save_key}.%(ext)s"
        try:
            with yt_dlp.YoutubeDL(yt_audio_extractor_opts) as ydl:
                ydl.download([yt_url])
                return f"{save_key}.wav"
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def download_video(save_dir: str, yt_url: str) -> Optional[str]:
        yt_video_extractor_opts["outtmpl"] = os.path.join(save_dir, f"video.%(ext)s")
        try:
            with yt_dlp.YoutubeDL(yt_video_extractor_opts) as ydl:
                ydl.download([yt_url])
                return yt_video_extractor_opts["outtmpl"]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def download_subtitle(subtitle_url: str) -> Optional[list[Segment]]:
        try:
            response = requests.get(subtitle_url)
            return YTHelper._yt_response_postprocessor(response.text)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def _yt_response_postprocessor(yt_response_text: str) -> list[Segment]:
        yt_response_dict = json.loads(yt_response_text)["events"]
        new_subtitle_list = []
        for seg in yt_response_dict:
            start_ms = seg["tStartMs"]
            duration_ms = seg["dDurationMs"]
            start = start_ms / 1000
            end = (start_ms + duration_ms) / 1000
            text = ",".join([sentence["utf8"] for sentence in seg["segs"]])
            new_subtitle_list.append(Segment(start=start, end=end, text=text))
        return new_subtitle_list
