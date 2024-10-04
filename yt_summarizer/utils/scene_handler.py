import os

from scenedetect import ContentDetector, detect
from scenedetect.frame_timecode import FrameTimecode

from yt_summarizer.models.video_fragment import SceneDetectionInfo

CONTENT_DETECTOR_THRESHOLD = 20.0
MINIMUM_SCENE_DURATION = 10.0
IMAGE_TIMESTAMP_OFFSET = 3.0


class SceneHandler:

    @staticmethod
    def _video_exists(video_path: str) -> bool:
        return os.path.exists(video_path)

    @classmethod
    def _scene_postprocessor(
        cls,
        scenedetect_result: list[tuple[FrameTimecode, FrameTimecode]],
    ) -> list[SceneDetectionInfo]:
        new_scenes: list[SceneDetectionInfo] = []
        for start_timecode, end_timecode in scenedetect_result:
            start_sec = start_timecode.get_seconds()
            end_sec = end_timecode.get_seconds()
            duration = end_sec - start_sec
            if duration < MINIMUM_SCENE_DURATION:
                continue

            img_timestamp = end_sec - IMAGE_TIMESTAMP_OFFSET
            new_scenes.append(
                SceneDetectionInfo(
                    start=start_sec, end=end_sec, img_timestamp=img_timestamp
                )
            )
        return new_scenes

    @classmethod
    def detect_scenes(cls, video_path: str) -> list[SceneDetectionInfo]:
        if not cls._video_exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        scenedetect_result = detect(
            video_path, ContentDetector(threshold=CONTENT_DETECTOR_THRESHOLD)
        )
        scene_result = cls._scene_postprocessor(scenedetect_result)
        return scene_result
