# image_models/image_viewer.py

import io

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QSlider


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_pixmap = None

    def initUI(self):
        # 窗口布局和样式
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)

        # 缩放滑动条
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 200)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.scaleImage)
        self.layout.addWidget(self.slider)

    def loadImage(self, image):
        if isinstance(image, str):
            self.original_pixmap = QPixmap(image)
        elif isinstance(image, QPixmap):
            self.original_pixmap = image
        elif isinstance(image, Image.Image):
            # 将PIL.Image.Image转换为QPixmap
            byte_io = io.BytesIO()
            image.save(byte_io, format='PNG')
            byte_io.seek(0)
            self.original_pixmap = QPixmap()
            self.original_pixmap.loadFromData(byte_io.getvalue())
        else:
            print("错误：无法识别的图像数据类型。")
            return

        if self.original_pixmap.isNull():
            print("错误：无法加载图像。")
            return

        self.image_label.setPixmap(self.original_pixmap)
        self.resizeImage()

    def resizeImage(self):
        if self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def zoomIn(self):
        self.slider.setValue(self.slider.value() + 10)

    def zoomOut(self):
        self.slider.setValue(self.slider.value() - 10)

    def scaleImage(self):
        if self.original_pixmap:
            scale_factor = self.slider.value() / 100.0
            scaled_pixmap = self.original_pixmap.scaled(self.original_pixmap.size() * scale_factor, Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resizeImage()
