"""设置页面模块"""

from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QHBoxLayout,
    QComboBox, QPushButton, QMessageBox, QLineEdit, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from utils import ThemeManager
from utils.messagebox import NMessageBox
from utils.pwd_utils import PasswordOperate
from utils.style import StyleButtonManager, StyleQComboBoxManager, StyleQLineEditManager
from .base_page import BasePage
import json
import os


class SettingsPage(BasePage):
    """设置页面"""
    
    # 定义信号
    theme_changed = pyqtSignal(str)  # 主题改变信号
    
    def __init__(self, key):
        # 先初始化主题数据，再调用父类初始化
        self.themes = ThemeManager().themes
        self.current_theme = "默认主题"
        self.load_theme_settings()
        self.encryption_key=key
        # 调用父类初始化（这会调用init_ui）
        super().__init__("设置")
    
    def init_ui(self):
        """初始化设置界面"""
        # 主题设置卡片
        theme_card = self.create_theme_settings_card()
        self.add_card(theme_card)
        # 修改密码
        passwd_card = self.create_passwd_settings_card()
        self.add_card(passwd_card)
        self.add_stretch()
    
    def create_theme_settings_card(self):
        """创建主题设置卡片"""
        theme_card = QFrame()
        theme_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                margin: 0px;
                padding: 5px;
            }
        """)
        theme_layout = QVBoxLayout(theme_card)
        # 主题设置标题
        theme_title = QLabel("🎨 界面主题")
        theme_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        theme_title.setStyleSheet("padding: 4px 0px; color: #333333; border: none;")
        theme_layout.addWidget(theme_title)

        # 主题选择区域内容卡片
        theme_content_layout = QVBoxLayout()

        # 主题选择标签
        theme_selection_layout = QGridLayout()
        theme_label = QLabel("选择主题:")
        theme_label.setFont(QFont("Microsoft YaHei", 10))
        theme_label.setStyleSheet("color: #666666;  border: none;")
        theme_label.setFixedWidth(100)
        theme_selection_layout.addWidget(theme_label,0,0)
        
        # 主题下拉菜单
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(self.themes.keys()))
        self.theme_combo.setCurrentText(self.current_theme)
        StyleQComboBoxManager.set_style_comboBox_default(self.theme_combo)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_selection_layout.addWidget(self.theme_combo,0,1)
        # 应用按钮
        apply_btn = QPushButton("应用主题")
        apply_btn.setFont(QFont("Microsoft YaHei", 10))
        StyleButtonManager.set_style_btn_sheet_default(apply_btn)
        apply_btn.clicked.connect(self.apply_theme)
        apply_btn.setFixedWidth(100)
        theme_selection_layout.addWidget(apply_btn,0,2)
        theme_content_layout.addLayout(theme_selection_layout)
        # 预览卡片
        preview_layout = QGridLayout()
        bg_label = QLabel("背景颜色:")
        bg_label.setFont(QFont("Microsoft YaHei", 10))
        bg_label.setStyleSheet("color: #666666;  border: none;")
        bg_label.setFixedWidth(100)
        self.preview_card = QFrame()
        self.update_preview_card()
        preview_layout.addWidget(bg_label, 0, 0)
        preview_layout.addWidget(self.preview_card,0,1)


        theme_content_layout.addLayout(preview_layout)
        #合成
        theme_layout.addLayout(theme_content_layout)
        return theme_card

    def create_passwd_settings_card(self):
        """创建密码设置卡片"""
        passwd_card = QFrame()
        passwd_card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                margin: 0px;
                padding: 5px;
            }
        """)
        passwd_layout = QVBoxLayout(passwd_card)
        passwd_layout.setSpacing(10)
        # 密码设置标题
        passwd_title = QLabel("🔒 密码设置")
        passwd_title.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        passwd_title.setStyleSheet("padding: 10px 0px; color: #333333; border: none;")
        passwd_layout.addWidget(passwd_title)

        passwd_input_layout=QGridLayout()

        passwd_input_layout.setVerticalSpacing(10)
        # 密码设置内容
        passwd_content = QLabel("初始密码")
        passwd_content.setFont(QFont("Microsoft YaHei", 10))
        passwd_content.setStyleSheet("color: #666666; border: none; ")
        # 密码设置输入框
        self.passwd_input = QLineEdit()
        self.passwd_input.setPlaceholderText("请输入旧的访问码...")
        StyleQLineEditManager.set_style_edit_default(self.passwd_input)
        self.passwd_input.setEchoMode(QLineEdit.Password)
        passwd_input_layout.addWidget(passwd_content, 0, 0)
        passwd_input_layout.addWidget(self.passwd_input, 0,1)

        # 新密码设置内容
        new_passwd_content = QLabel("新密码：")
        new_passwd_content.setFont(QFont("Microsoft YaHei", 10))
        new_passwd_content.setStyleSheet("color: #666666; border: none; ")
        # 密码设置输入框
        self.new_passwd_input = QLineEdit()
        StyleQLineEditManager.set_style_edit_default(self.new_passwd_input)
        self.new_passwd_input.setPlaceholderText("请输入新的访问码...")
        self.new_passwd_input.setEchoMode(QLineEdit.Password)
        passwd_input_layout.addWidget(new_passwd_content, 1, 0)
        passwd_input_layout.addWidget(self.new_passwd_input, 1,1)

        # 新密码设置内容
        reset_passwd_content = QLabel("确认密码：")
        reset_passwd_content.setFont(QFont("Microsoft YaHei", 10))
        reset_passwd_content.setStyleSheet("color: #666666; border: none; ")

        # 密码设置输入框
        self.reset_passwd_input = QLineEdit()
        self.reset_passwd_input.setPlaceholderText("请再次输入访问码...")
        StyleQLineEditManager.set_style_edit_default(self.reset_passwd_input)
        self.reset_passwd_input.setEchoMode(QLineEdit.Password)
        passwd_input_layout.addWidget(reset_passwd_content, 2, 0)
        passwd_input_layout.addWidget(self.reset_passwd_input, 2,1)
        passwd_layout.addLayout(passwd_input_layout)

        passwd_layout.addSpacing(10)
        # 密码设置确认按钮
        passwd_confirm_btn = QPushButton("确认设置")
        passwd_confirm_btn.setFont(QFont("Microsoft YaHei", 10))
        StyleButtonManager.set_style_btn_sheet_default(passwd_confirm_btn)
        passwd_confirm_btn.clicked.connect(self.change_passwd_key)
        passwd_layout.addWidget(passwd_confirm_btn)
        return passwd_card

    def update_preview_card(self):
        """更新预览卡片"""
        selected_theme = self.theme_combo.currentText() if hasattr(self, 'theme_combo') else self.current_theme
        theme_colors = self.themes.get(selected_theme, self.themes["默认主题"])
        
        self.preview_card.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_colors['background']};
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


    def change_passwd_key(self):
        pwd_operate=PasswordOperate(self.encryption_key)
        pwd_operate.changePwd(
            self.passwd_input.text(),
            self.new_passwd_input.text(),
            self.reset_passwd_input.text()
        )
