from typing import Optional

import whisperx


class WhisperxHandler:
    device = "cuda"
    compute_type = "float16"
    batch_size = 4
    model_dir = "./path/"
    model = whisperx.load_model(
        "large-v3",
        device,
        compute_type=compute_type,
        download_root=model_dir,
    )

    @classmethod
    def transcribe(cls, audio_path: str) -> Optional[dict]:
        try:
            audio = whisperx.load_audio(audio_path)
            result = cls.model.transcribe(audio, batch_size=cls.batch_size)
            return cls._preprocess_subtitle(result)
        except Exception as e:
            print(f"An error during whisperx transcription: {e}")
            return None

    @staticmethod
    def _preprocess_subtitle(whisperx_result: dict) -> str:
        return "\n".join([seg["text"] for seg in whisperx_result["segments"]])
