# utils/ocr_thread.py

from PyQt5.QtCore import pyqtSignal, QThread
from image_models.image_ocr_processor import ImageOCRProcessor


class OCRThread(QThread):
    result_signal = pyqtSignal(object)

    def __init__(self, image_path, api_token, email, log_box, image_size, char_ocr, det_mode, return_position, return_choices):
        super().__init__()
        self.image_path = image_path
        self.ocr_processor = ImageOCRProcessor(api_token, email, log_box)
        self.image_size = image_size
        self.char_ocr = char_ocr
        self.det_mode = det_mode
        self.return_position = return_position
        self.return_choices = return_choices
        self.log_box = log_box

    def run(self):
        response = self.ocr_processor.process_single_image(self.image_path, self.image_size, self.char_ocr,
                                                           self.det_mode, self.return_position, self.return_choices)
        self.result_signal.emit(response)
