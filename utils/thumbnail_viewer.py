# utils/thumbnail_viewer.py

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout


class ThumbnailViewer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.setScaledContents(False)
        self.current_scale_factor = 1.0
        self.is_zoomed_in = False

    def setThumbnail(self, pixmap, size=None):
        self.original_pixmap = pixmap
        self.current_scale_factor = 1.0
        self.is_zoomed_in = False
        self.updateThumbnail(size)

    def updateThumbnail(self, size):
        if self.original_pixmap and not self.original_pixmap.isNull():
            if isinstance(size, QSize):  # 确保 size 是 QSize 对象
                scaled_pixmap = self.original_pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                scaled_pixmap = self.original_pixmap
            self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.original_pixmap:
            self.showZoomedDialog()

    def showZoomedDialog(self):
        if self.original_pixmap:
            dialog = QDialog(self)
            dialog.setWindowTitle("放大图像")
            layout = QVBoxLayout()
            label = QLabel()
            label.setPixmap(self.original_pixmap)
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.exec_()  # 显示为模态对话框

    def resizeEvent(self, event):
        if not self.is_zoomed_in:
            self.updateThumbnail(self.size())
