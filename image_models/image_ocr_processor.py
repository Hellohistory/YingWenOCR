# image_models/image_ocr_processor.py

import base64

import requests


class ImageOCRProcessor:
    def __init__(self, api_token, email, log_box):
        self.api_token = api_token
        self.email = email
        self.log_box = log_box

    def process_single_image(self, image_path, image_size, char_ocr, det_mode, return_position, return_choices):
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        data = {
            'image': base64_image,
            'token': self.api_token,
            'email': self.email,
            'image_size': image_size,
            'char_ocr': char_ocr,
            'det_mode': det_mode,
            'return_position': return_position,
            'return_choices': return_choices,
        }

        response = requests.post('https://images.kandianguji.com:14141/ocr_api', data=data)
        if response.status_code == 200:
            return response.json()
        else:
            self.log_box.log(f'响应失败，状态码：{response.status_code}')
            self.log_box.log(response.text)
            return None
