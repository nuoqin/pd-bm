"""验证码输入对话框模块"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from utils.crypto_utils import CryptoAesUtils
from utils.style import StyleButtonManager





class VerificationDialog(QDialog):
    """验证码输入对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.encryption_key = None
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("访问码")
        self.setModal(True)
        self.setFixedSize(400, 200)
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 只显示关闭按钮

        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 12px;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            QLineEdit {
                border: 1px solid #dee2e6;
                border-radius: 2px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #007acc;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 2px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 说明文字
        desc_label = QLabel("此码将用于加密和解密您的数据")
        desc_label.setFont(QFont("Microsoft YaHei", 10))
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #666666;")
        layout.addWidget(desc_label)

        # 输入区域
        input_layout = QVBoxLayout()
        input_layout.setSpacing(8)
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("输入访问码...")
        self.input_edit.setEchoMode(QLineEdit.Password)
        input_layout.addWidget(self.input_edit)
        layout.addLayout(input_layout)
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 确认按钮
        confirm_btn = QPushButton("确认")
        StyleButtonManager.set_style_btn_sheet_default(confirm_btn)
        confirm_btn.clicked.connect(self.confirm_password)

        button_layout.addStretch()
        button_layout.addWidget(confirm_btn)
        layout.addLayout(button_layout)
        # 设置焦点
        self.input_edit.setFocus()

    def confirm_password(self):
        """确认输入的密码"""
        password = self.input_edit.text().strip()
        if not password:
            QMessageBox.warning(self, "输入错误", "请输入访问码！")
            return

        if len(password) < 4:
            QMessageBox.warning(self, "密码太短", "访问码至少需要4个字符！")
            return
        # 使用用户输入的密码直接作为加密密钥的基础
        self.encryption_key = CryptoAesUtils.generate_key_from_password(password)
        self.accept()

    def get_encryption_key(self) -> str:
        """获取加密密钥"""
        return getattr(self, 'encryption_key', None)

    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.confirm_password()
        else:
            super().keyPressEvent(event)
