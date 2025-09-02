"""基础页面类模块"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class BasePage(QWidget):
    """基础页面类，提供通用的页面布局和功能"""
    
    def __init__(self, title="页面"):
        super().__init__()
        self.title = title
        self.setStyleSheet("background-color: transparent;")  # 透明背景
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # 去除页面边距
        
        # 初始化页面内容
        self.init_ui()
    
    def init_ui(self):
        """子类需要重写此方法来实现具体的界面内容"""
        pass
    
    def create_card(self, text, bold=False, size=14):
        """创建单个圆角卡片"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #dddddd;
                margin: 0px;
                padding: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        
        label = QLabel(text)
        font = QFont("Microsoft YaHei", size)
        if bold:
            font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        
        card_layout.addWidget(label)
        return card
    
    def add_card(self, card):
        """添加卡片到页面"""
        self.main_layout.addWidget(card)
    
    def add_stretch(self):
        """添加伸缩空间"""
        self.main_layout.addStretch()
