# utils/ocr_display.py
from utils.logs import LogBox


class OCRDisplay:
    def __init__(self, result_textbox):
        self.result_textbox = result_textbox
        self.log_box = LogBox()

    def display_result(self, ocr_response):
        self.log_box.log("开始显示OCR结果")
        self.result_textbox.clear()
        ocr_texts = ocr_response['data']['texts']
        for text in ocr_texts:
            self.log_box.log(f"添加文本: {text}")
            self.result_textbox.append(text)
        self.log_box.log("OCR结果显示完成")
