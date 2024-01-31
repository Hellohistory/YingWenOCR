# image_processing_thread.py

from PyQt5.QtCore import QThread, pyqtSignal
from image_processor import ImageProcessor


class ImageProcessingThread(QThread):
    finished_signal = pyqtSignal(object, list)

    def __init__(self, image_path, ocr_data):
        super().__init__()
        self.image_path = image_path
        self.ocr_data = ocr_data

    def run(self):
        processor = ImageProcessor(self.image_path, self.ocr_data)
        boxed_image, words_data = processor.process_image()

        # 直接发送boxed_image作为PIL图像对象
        self.finished_signal.emit(boxed_image, words_data)
