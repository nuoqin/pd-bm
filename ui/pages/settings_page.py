"""设置页面模块"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QHBoxLayout, 
    QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from utils.messagebox import NMessageBox
from .base_page import BasePage
import json
import os


class SettingsPage(BasePage):
    """设置页面"""
    
    # 定义信号
    theme_changed = pyqtSignal(str)  # 主题改变信号
    
    def __init__(self):
        # 先初始化主题数据，再调用父类初始化
        self.themes = {
            "默认主题": {
                "background": "#f5f7fa",
                "card_background": "#ffffff",
                "text_color": "#333333",
                "border_color": "#dddddd",
                "accent_color": "#007acc"
            },
            "深色主题": {
                "background": "#2b2b2b",
                "card_background": "#3c3c3c",
                "text_color": "#ffffff",
                "border_color": "#555555",
                "accent_color": "#4a9eff"
            },
            "护眼主题": {
                "background": "#f0f8e8",
                "card_background": "#ffffff",
                "text_color": "#2d5016",
                "border_color": "#c8e6c9",
                "accent_color": "#4caf50"
            },
            "温暖主题": {
                "background": "#fff8e1",
                "card_background": "#ffffff",
                "text_color": "#5d4037",
                "border_color": "#ffcc02",
                "accent_color": "#ff9800"
            },
            "清新主题": {
                "background": "#e3f2fd",
                "card_background": "#ffffff",
                "text_color": "#0d47a1",
                "border_color": "#90caf9",
                "accent_color": "#2196f3"
            }
        }
        self.current_theme = "默认主题"
        self.load_theme_settings()
        
        # 调用父类初始化（这会调用init_ui）
        super().__init__("设置")
    
    def init_ui(self):
        """初始化设置界面"""

        # 主题设置卡片
        theme_card = self.create_theme_settings_card()
        self.add_card(theme_card)

        # 其他设置选项卡片
        other_settings_card = QFrame()
        other_settings_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #dddddd;
                margin: 0px;
                padding: 20px;
            }
        """)
        self.add_card(other_settings_card)
        self.add_stretch()
    
    def create_theme_settings_card(self):
        """创建主题设置卡片"""
        theme_card = QFrame()
        theme_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 12px;
                border: 1px solid #dddddd;
                margin: 0px;
                padding: 20px;
            }
        """)
        theme_layout = QVBoxLayout(theme_card)
        
        # 主题设置标题
        theme_title = QLabel("🎨 界面主题")
        theme_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        theme_title.setStyleSheet("padding: 8px 0px; color: #333333; border: none;")
        theme_layout.addWidget(theme_title)
        
        # 主题选择区域
        theme_selection_layout = QHBoxLayout()
        
        # 主题选择标签
        theme_label = QLabel("选择主题:")
        theme_label.setFont(QFont("Microsoft YaHei", 12))
        theme_label.setStyleSheet("color: #666666;  border: none;")
        theme_selection_layout.addWidget(theme_label)
        
        # 主题下拉菜单
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(self.themes.keys()))
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.setFont(QFont("Microsoft YaHei", 11))
        self.theme_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: #ffffff;
                color: #333333;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #007acc;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666666;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dee2e6;
                background-color: #ffffff;
                selection-background-color: #007acc;
                selection-color: white;
            }
        """)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_selection_layout.addWidget(self.theme_combo)
        
        # 应用按钮
        apply_btn = QPushButton("应用主题")
        apply_btn.setFont(QFont("Microsoft YaHei", 11))
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        apply_btn.clicked.connect(self.apply_theme)
        theme_selection_layout.addWidget(apply_btn)
        
        theme_selection_layout.addStretch()
        theme_layout.addLayout(theme_selection_layout)
        # 预览卡片
        self.preview_card = QFrame()
        self.update_preview_card()
        theme_layout.addWidget(self.preview_card)

        return theme_card
    
    def update_preview_card(self):
        """更新预览卡片"""
        selected_theme = self.theme_combo.currentText() if hasattr(self, 'theme_combo') else self.current_theme
        theme_colors = self.themes.get(selected_theme, self.themes["默认主题"])
        
        self.preview_card.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_colors['card_background']};
                border: 1px solid {theme_colors['border_color']};
                border-radius: 2px;
                padding: 15px;
                margin: 5px 0px;
            }}
        """)
        
        # 清除现有布局
        if self.preview_card.layout():
            while self.preview_card.layout().count():
                child = self.preview_card.layout().takeAt(0)
                if child.widget():
                    child.widget().setParent(None)
        else:
            preview_layout = QVBoxLayout(self.preview_card)
            
        preview_layout = self.preview_card.layout() or QVBoxLayout(self.preview_card)
        
        # 预览内容
        preview_title = QLabel("示例卡片")
        preview_title.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        preview_title.setStyleSheet(f"color: {theme_colors['text_color']};")
        preview_layout.addWidget(preview_title)
        
        preview_text = QLabel("这是主题预览效果，显示当前主题的颜色搭配")
        preview_text.setFont(QFont("Microsoft YaHei", 10))
        preview_text.setStyleSheet(f"color: {theme_colors['text_color']}; opacity: 0.8;")
        preview_layout.addWidget(preview_text)
        
        # 预览按钮
        preview_btn = QPushButton("示例按钮")
        preview_btn.setFont(QFont("Microsoft YaHei", 10))
        preview_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme_colors['accent_color']};
                color: white;
                border: none;
                padding: 4px 12px;
                border-radius: 4px;
                max-width: 100px;
            }}
        """)
        preview_layout.addWidget(preview_btn)
    
    def on_theme_changed(self, theme_name):
        """主题选择改变时的处理"""
        self.update_preview_card()
    
    def apply_theme(self):
        """应用选中的主题"""
        selected_theme = self.theme_combo.currentText()
        if selected_theme != self.current_theme:
            self.current_theme = selected_theme
            self.save_theme_settings()
            self.theme_changed.emit(selected_theme)
            NMessageBox.information(self, "主题设置", f"已应用 {selected_theme}！\n重启应用后完全生效。")
    
    def load_theme_settings(self):
        """加载主题设置"""
        try:
            settings_file = "config/theme_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('current_theme', '默认主题')
        except Exception as e:
            print(f"加载主题设置失败: {e}")
            self.current_theme = "默认主题"
    
    def save_theme_settings(self):
        """保存主题设置"""
        try:
            settings = {
                'current_theme': self.current_theme
            }
            # 确保config目录存在
            os.makedirs('config', exist_ok=True)
            
            with open('config/theme_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存主题设置失败: {e}")
    
    def get_current_theme_colors(self):
        """获取当前主题的颜色配置"""
        return self.themes.get(self.current_theme, self.themes["默认主题"])
