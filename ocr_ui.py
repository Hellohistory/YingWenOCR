from PyQt5.QtWidgets import QTableWidget, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGroupBox, QRadioButton, \
    QCheckBox, QWidget, QSizePolicy, QTextEdit
from utils.thumbnail_viewer import ThumbnailViewer
from image_models.image_viewer import ImageViewer
from utils.logs import LogBox


class OCRUi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("影文OCR")
        # self.setWindowIcon(QIcon('path/to/logo.png'))  # 设置窗口图标，暂时注释
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # 左侧布局：设置与日志区
        left_layout = QVBoxLayout()

        # 文件选择按钮
        self.btn_select_file = QPushButton('选择文件')
        left_layout.addWidget(self.btn_select_file)

        # API Token 输入框
        self.api_token_input = QLineEdit(self)
        left_layout.addWidget(QLabel('API Token:'))
        left_layout.addWidget(self.api_token_input)

        # Email 输入框
        self.email_input = QLineEdit(self)
        left_layout.addWidget(QLabel('Email:'))
        left_layout.addWidget(self.email_input)

        # 修改后的文字排版方向下拉菜单
        self.det_mode_combo = QComboBox(self)
        self.det_mode_combo.addItem("自动", "auto")
        self.det_mode_combo.addItem("竖排", "sp")
        self.det_mode_combo.addItem("横排", "hp")
        left_layout.addWidget(QLabel('文字排版方向:'))
        left_layout.addWidget(self.det_mode_combo)

        # 选择检测模式
        self.det_mode_group = QGroupBox("检测模式")
        det_mode_layout = QHBoxLayout()
        self.char_det_radio = QRadioButton("单字检测识别")
        self.line_det_radio = QRadioButton("文本行检测识别")
        self.char_det_radio.setChecked(True)  # 默认选择单字检测
        det_mode_layout.addWidget(self.char_det_radio)
        det_mode_layout.addWidget(self.line_det_radio)
        self.det_mode_group.setLayout(det_mode_layout)
        left_layout.addWidget(self.det_mode_group)

        # 图片尺寸调节输入框
        self.image_size_input = QLineEdit(self)
        self.image_size_input.setText("1024")  # 默认值为1024
        left_layout.addWidget(QLabel('图片尺寸调节:'))
        left_layout.addWidget(self.image_size_input)

        # 是否保存设置勾选框
        self.save_settings_checkbox = QCheckBox("保存设置")
        self.save_settings_checkbox.setChecked(True)
        left_layout.addWidget(self.save_settings_checkbox)

        # 执行OCR按钮
        self.btn_execute = QPushButton('执行OCR')
        left_layout.addWidget(self.btn_execute)

        # 日志框
        self.log_box = LogBox()
        left_layout.addWidget(QLabel('运行日志'))
        left_layout.addWidget(self.log_box)
        # 中间布局：图片展示区
        middle_layout = QVBoxLayout()
        self.image_viewer = ImageViewer()
        self.image_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        middle_layout.addWidget(self.image_viewer)

        # 右侧布局：OCR内容展示区
        right_layout = QVBoxLayout()
        self.ocr_result_textbox = QTextEdit()
        self.ocr_result_textbox.setReadOnly(True)
        right_layout.addWidget(QLabel('OCR内容'))
        right_layout.addWidget(self.ocr_result_textbox)

        # 表格
        self.ocr_table = QTableWidget(self)
        self.ocr_table.setColumnCount(3)
        self.ocr_table.setHorizontalHeaderLabels(['图像', 'OCR内容', '置信度'])
        right_layout.addWidget(self.ocr_table)

        # 创建 ThumbnailViewer 实例并添加到布局中
        self.thumbnail_viewer = ThumbnailViewer()
        self.thumbnail_viewer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        right_layout.addWidget(self.thumbnail_viewer)  # 添加缩略图视图

        # 添加布局到主布局
        main_layout.addLayout(left_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(right_layout)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)
        main_layout.setStretch(2, 1)

        # 窗口默认大小
        self.setMinimumSize(1400, 900)
        self.api_token_input.setMinimumWidth(200)
        self.email_input.setMinimumWidth(200)
