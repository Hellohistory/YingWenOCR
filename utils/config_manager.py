# utils/config_manager.py

from PyQt5.QtCore import QSettings


class ConfigManager:
    def __init__(self, filename="config.ini"):
        self.settings = QSettings(filename, QSettings.IniFormat)

    def load_settings(self):
        """从 config.ini 文件中读取设置"""
        return {
            "api_token": self.settings.value("api_token", ""),
            "email": self.settings.value("email", ""),
            "det_mode": self.settings.value("det_mode", "auto"),
            "image_size": int(self.settings.value("image_size", 1024)),
            "char_ocr": self.settings.value("char_ocr", True, type=bool),
            "return_position": self.settings.value("return_position", True, type=bool),
            "return_choices": self.settings.value("return_choices", True, type=bool)
        }

    def save_settings(self, api_token, email, det_mode, image_size, char_ocr, return_position, return_choices):
        """将设置保存到 config.ini 文件中"""
        self.settings.setValue("api_token", api_token)
        self.settings.setValue("email", email)
        self.settings.setValue("det_mode", det_mode)
        self.settings.setValue("image_size", image_size)
        self.settings.setValue("char_ocr", char_ocr)
        self.settings.setValue("return_position", return_position)
        self.settings.setValue("return_choices", return_choices)
