# image_models/ocr_table_updater.py

from PIL import Image, ImageDraw


class OCRTablerUpdater:
    def __init__(self, image, ocr_data):
        # 如果image是Image对象，则直接使用，否则，尝试打开文件
        if isinstance(image, Image.Image):
            self.image = image
        else:
            self.image_path = image
            self.image = Image.open(self.image_path)

        # 直接使用传入的OCR数据字典
        self.ocr_data = ocr_data

    def _calculate_scale(self):
        ocr_height = self.ocr_data['data']['height']
        ocr_width = self.ocr_data['data']['width']
        actual_width, actual_height = self.image.size
        scale_width = ocr_width / actual_width
        scale_height = ocr_height / actual_height
        return scale_width, scale_height

    def update_table(self):
        scale_width, scale_height = self._calculate_scale()
        draw = ImageDraw.Draw(self.image)

        for line in self.ocr_data['data']['text_lines']:
            (x1, y1), (x3, y3) = line['position'][0], line['position'][2]
            adjusted_x1, adjusted_y1 = int(x1 / scale_width), int(y1 / scale_height)
            adjusted_x3, adjusted_y3 = int(x3 / scale_width), int(y3 / scale_height)

            # 确保坐标顺序正确
            adjusted_x1, adjusted_x3 = min(adjusted_x1, adjusted_x3), max(adjusted_x1, adjusted_x3)
            adjusted_y1, adjusted_y3 = min(adjusted_y1, adjusted_y3), max(adjusted_y1, adjusted_y3)

            draw.rectangle([adjusted_x1, adjusted_y1, adjusted_x3, adjusted_y3], outline='red', width=3)

        return self.image
