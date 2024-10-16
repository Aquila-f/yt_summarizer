import os

from cv2 import CAP_PROP_POS_MSEC, VideoCapture, imwrite
from scenedetect import ContentDetector, detect
from scenedetect.frame_timecode import FrameTimecode

from yt_summarizer.llm_parser.image_key_parser import ImageKeyParser
from yt_summarizer.models.llm_response import ImageKeyResponse
from yt_summarizer.models.video_fragment import SceneDetectionInfo, SceneExtractInfo
from yt_summarizer.utils.file_operation import is_exist

CONTENT_DETECTOR_THRESHOLD = 15.0
MINIMUM_SCENE_DURATION = 5.0
IMAGE_TIMESTAMP_OFFSET = 1.2


class SceneHandler:
    @staticmethod
    def _extract_key_from_image(image_path: str) -> ImageKeyResponse:
        try:
            response = ImageKeyParser().parse(image_path)
            return response
        except Exception as e:
            print(f"Error extracting key from image: {e}")
            return ImageKeyResponse(content="", key="")

    @classmethod
    def _post_process_img_extract(
        cls,
        scene_result: list[SceneDetectionInfo],
    ) -> list[SceneExtractInfo]:
        scene_extract_result = []
        for scene in scene_result:
            response = cls._extract_key_from_image(scene.img_path)
            scene_extract_result.append(
                SceneExtractInfo(
                    **scene.model_dump(),
                    key=response.key,
                    has_chart=response.has_chart,
                    llm_response=response.content.split("\n"),
                )
            )
        return scene_extract_result

    @classmethod
    def _scene_postprocessor(
        cls,
        save_root: str,
        scenedetect_result: list[tuple[FrameTimecode, FrameTimecode]],
    ) -> list[SceneDetectionInfo]:
        new_scenes: list[SceneDetectionInfo] = []
        for start_timecode, end_timecode in scenedetect_result:
            start_sec = start_timecode.get_seconds()
            end_sec = end_timecode.get_seconds()
            duration = end_sec - start_sec
            if duration < MINIMUM_SCENE_DURATION:
                continue

            img_timestamp = round((end_sec - IMAGE_TIMESTAMP_OFFSET) * 1000)
            scene_path = cls._save_scene_images_by_sec(save_root, img_timestamp)

            new_scenes.append(
                SceneDetectionInfo(
                    start=start_sec,
                    end=end_sec,
                    img_path=scene_path,
                    img_timestamp=img_timestamp,
                )
            )
        return new_scenes

    @staticmethod
    def _save_scene_images_by_sec(output_dir: str, ms: float) -> str:
        video_path = os.path.join(output_dir, "video.mp4")
        scenes_dir = os.path.join(output_dir, "scenes")

        if not os.path.exists(scenes_dir):
            os.makedirs(scenes_dir)

        video_capture = VideoCapture(video_path)
        video_capture.set(CAP_PROP_POS_MSEC, ms)
        success, frame_image = video_capture.read()
        if not success:
            raise ValueError("Failed to read frame from video")

        img_path = os.path.join(scenes_dir, f"{ms}.png")
        imwrite(img_path, frame_image)
        return img_path

    @classmethod
    def detect_scenes(cls, save_dir: str) -> list[SceneDetectionInfo]:
        video_path = os.path.join(save_dir, "video.mp4")
        if not is_exist(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        scenedetect_result = detect(
            video_path, ContentDetector(threshold=CONTENT_DETECTOR_THRESHOLD)
        )

        scene_result = cls._scene_postprocessor(save_dir, scenedetect_result)
        return scene_result

    @classmethod
    def extract_scenes(cls, save_dir: str) -> list[SceneExtractInfo]:
        scene_result = cls.detect_scenes(save_dir)
        scene_extract_result = cls._post_process_img_extract(scene_result)
        return scene_extract_result
