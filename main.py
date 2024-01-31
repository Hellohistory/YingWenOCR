import sys

from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem

from utils.config_manager import ConfigManager
from ocr_ui import OCRUi
from utils.thumbnail_viewer import ThumbnailViewer
from utils.image_processing_thread import ImageProcessingThread  # 导入新的图像处理线程
from utils.ocr_display import OCRDisplay
from utils.ocr_thread import OCRThread


class OCRApp(OCRUi):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.config_manager = ConfigManager()
        self.btn_select_file.clicked.connect(self.openFileNameDialog)
        self.btn_execute.clicked.connect(self.executeOCR)
        self.ocr_display = OCRDisplay(self.ocr_result_textbox)
        self.loadSettings()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "",
                                                  "All Files (*);;Image Files (*.png *.jpg *.jpeg)", options=options)
        if fileName:
            self.image_path = fileName
            self.image_viewer.loadImage(fileName)

    def loadSettings(self):
        settings = self.config_manager.load_settings()
        self.api_token_input.setText(settings["api_token"])
        self.email_input.setText(settings["email"])
        self.det_mode_combo.setCurrentIndex(self.det_mode_combo.findData(settings["det_mode"]))
        self.image_size_input.setText(str(settings["image_size"]))
        self.char_det_radio.setChecked(settings["char_ocr"])
        self.line_det_radio.setChecked(not settings["char_ocr"])

    def saveSettings(self):
        if self.save_settings_checkbox.isChecked():
            det_mode = self.det_mode_combo.currentData()
            image_size = int(self.image_size_input.text())
            char_ocr = self.char_det_radio.isChecked()
            return_position = True  # 根据需要设置
            return_choices = True  # 根据需要设置
            self.config_manager.save_settings(self.api_token_input.text(), self.email_input.text(),
                                              det_mode, image_size, char_ocr, return_position, return_choices)

    def executeOCR(self):
        self.log_box.log("开始执行OCR...")
        if self.image_path is None:
            self.log_box.log("错误：未选择文件。请先选择一个图像文件。")
            return

        api_token = self.api_token_input.text()
        email = self.email_input.text()
        det_mode = self.det_mode_combo.currentData()
        char_ocr = self.char_det_radio.isChecked()
        image_size = int(self.image_size_input.text())
        return_position = True
        return_choices = True

        self.ocr_thread = OCRThread(self.image_path, api_token, email, self.log_box,
                                    image_size, char_ocr, det_mode, return_position, return_choices)
        self.ocr_thread.result_signal.connect(self.onOCRComplete)
        self.ocr_thread.start()

        self.saveSettings()

    def onOCRComplete(self, response):
        if response:
            self.ocr_display.display_result(response)
            self.image_processing_thread = ImageProcessingThread(self.image_path, response)
            self.image_processing_thread.finished_signal.connect(self.onImageProcessingComplete)
            self.image_processing_thread.start()
            self.log_box.log("OCR处理完成")
        else:
            self.log_box.log("OCR处理失败")

    def onImageProcessingComplete(self, boxed_image, words_data):
        # 处理 words_data 更新 OCR 表格
        if isinstance(words_data, list):
            self.updateOCRTable(words_data)
        else:
            self.log_box.log("错误：words_data 不是列表类型。")

        # 将 boxed_image (PIL图像) 传递给 ImageViewer
        self.image_viewer.loadImage(boxed_image)  # 使用 ImageViewer 的 loadImage 方法

    def updateOCRTable(self, words_data):
        self.ocr_table.setRowCount(len(words_data))
        for row, word_data in enumerate(words_data):
            if isinstance(word_data, dict) and {'image', 'text', 'confidence'}.issubset(word_data):
                # 显示裁剪后的图像
                cropped_image = word_data['image']

                # 将 PIL 图像转换为 QByteArray
                byte_array = QByteArray()
                buffer = QBuffer(byte_array)
                buffer.open(QIODevice.WriteOnly)
                cropped_image.save(buffer, 'PNG')  # 保存为 PNG 格式
                buffer.close()

                pixmap = QPixmap()
                pixmap.loadFromData(byte_array, 'PNG')

                # 创建 ThumbnailViewer 实例并设置 QPixmap
                thumbnail_viewer = ThumbnailViewer()
                thumbnail_viewer.setThumbnail(pixmap)

                # 将 ThumbnailViewer 添加到表格中
                self.ocr_table.setCellWidget(row, 0, thumbnail_viewer)

                # 显示文字内容
                text_item = QTableWidgetItem(word_data['text'])
                self.ocr_table.setItem(row, 1, text_item)

                # 显示置信度
                confidence_item = QTableWidgetItem(str(word_data['confidence']))
                self.ocr_table.setItem(row, 2, confidence_item)
            else:
                self.log_box.log(f"错误：无效的词条数据格式（行 {row}）。")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OCRApp()
    ex.show()
    sys.exit(app.exec_())
