from picamera2 import Picamera2
from PIL import Image


class Camera(Picamera2):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = self.create_still_configuration()
        self.configure(config)
        self.start()

    def get_image(self):
        image_array = self.capture_array()
        return Image.fromarray(image_array)
