from typing import Optional

import whisperx

from yt_summarizer.models.yt_info import Segment

CHUNK_SIZE = 10


class WhisperxHandler:
    device = "cuda"
    compute_type = "float16"
    batch_size = 4
    model_dir = "./path/"
    asr_options = {
        "initial_prompt": "你好，这是一个关于 金融逐字稿的討論。",
    }
    model = whisperx.load_model(
        "large-v3",
        device,
        compute_type=compute_type,
        download_root=model_dir,
        language="zh",
        asr_options=asr_options,
    )

    @classmethod
    def transcribe(cls, audio_path: str) -> Optional[list[Segment]]:
        try:
            audio = whisperx.load_audio(audio_path)
            result = cls.model.transcribe(
                audio, batch_size=cls.batch_size, chunk_size=CHUNK_SIZE
            )
            return cls._whisperx_postprocessor(result)
        except Exception as e:
            print(f"[[[ERROR]]] An error during whisperx transcription: {e}")
            return None

    @staticmethod
    def _whisperx_postprocessor(whisperx_result: dict) -> list[Segment]:
        segment_list: list[Segment] = []
        for segment in whisperx_result["segments"]:
            segment_list.append(
                Segment(
                    start=segment["start"],
                    end=segment["end"],
                    text=segment["text"],
                )
            )
        return segment_list
