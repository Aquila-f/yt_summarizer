from typing import Optional

import yt_dlp

from yt_summarizer.models.yt_info import YTInfo

ydl_opts = {}

yt_audio_extractor = yt_dlp.YoutubeDL(ydl_opts)


def get_youtube_object(user_query_url: str) -> Optional[dict]:
    try:
        info_dict = yt_audio_extractor.extract_info(user_query_url, download=False)
        return YTInfo(
            title=info_dict["title"],
            length=info_dict["duration"],
            author=info_dict["uploader"],
            channel_url=info_dict["channel_url"],
            thumbnail_url=info_dict["thumbnail"],
            views=info_dict["view_count"],
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
