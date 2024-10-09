import base64
import io

from PIL import Image


class ImageHandler:
    ZOOM_OUT_FACTOR = 3

    @classmethod
    def resize_and_convert_image_to_base64(cls, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            image = Image.open(image_file)
            resized_image = cls.resize_image(image, cls.ZOOM_OUT_FACTOR)
        return cls.to_base64(cls.to_bytes(resized_image))

    @staticmethod
    def resize_image(image: Image.Image, factor: float) -> Image.Image:
        new_size = (image.size[0] // factor, image.size[1] // factor)
        image = image.resize(new_size)
        return image

    @staticmethod
    def to_bytes(image: Image.Image) -> bytes:
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format="PNG")
        return img_byte_array.getvalue()

    @staticmethod
    def to_base64(image_bytes: bytes) -> str:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"
