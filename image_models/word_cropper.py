# image_models/word_cropper.py

class WordCropper:
    def __init__(self, image, ocr_data, scale_width, scale_height):
        self.image = image
        self.ocr_data = ocr_data
        self.scale_width = scale_width
        self.scale_height = scale_height

    def crop_words(self):
        words_data = []
        for line in self.ocr_data['data']['text_lines']:
            for word in line['words']:
                word_x1, word_y1, word_x2, word_y2 = word['position']
                adjusted_word_x1 = int(word_x1 / self.scale_width)
                adjusted_word_y1 = int(word_y1 / self.scale_height)
                adjusted_word_x2 = int(word_x2 / self.scale_width)
                adjusted_word_y2 = int(word_y2 / self.scale_height)
                cropped_image = self.image.crop((adjusted_word_x1, adjusted_word_y1, adjusted_word_x2, adjusted_word_y2))
                words_data.append({
                    'image': cropped_image,
                    'text': word['text'],
                    'confidence': word['confidence']
                })
        return words_data
