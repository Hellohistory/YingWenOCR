# image_ocr_processor.py

from image_models.ocr_table_updater import OCRTablerUpdater
from image_models.word_cropper import WordCropper
from PIL import Image


class ImageProcessor:
    def __init__(self, image_path, ocr_data):
        self.image_path = image_path
        self.ocr_data = ocr_data

    def process_image(self):
        image = Image.open(self.image_path)

        # 使用 OCRTablerUpdater 来框选文本行
        updater = OCRTablerUpdater(image, self.ocr_data)
        boxed_image = updater.update_table()  # 处理图像并返回图像对象

        # 使用 WordCropper 来处理单个字的切割
        scale_width, scale_height = updater._calculate_scale()
        cropper = WordCropper(boxed_image, updater.ocr_data, scale_width, scale_height)
        words_data = cropper.crop_words()

        # 返回处理后的图像对象和文字数据
        return boxed_image, words_data
