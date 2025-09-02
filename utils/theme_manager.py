"""主题管理器模块"""

import json
import os
from typing import Dict, Any


class ThemeManager:
    """主题管理器"""
    
    def __init__(self):
        self.themes = {
            "默认主题": {
                "background": "#f5f7fa",
                "card_background": "#ffffff",
                "text_color": "#333333",
                "border_color": "#dddddd",
                "accent_color": "#007acc",
                "hover_color": "#005a9e",
                "pressed_color": "#004080",
                "input_background": "#ffffff",
                "input_border": "#dee2e6",
                "secondary_text": "#666666"
            },
            "深色主题": {
                "background": "#2b2b2b",
                "card_background": "#3c3c3c",
                "text_color": "#ffffff",
                "border_color": "#555555",
                "accent_color": "#4a9eff",
                "hover_color": "#3d8bfd",
                "pressed_color": "#0d6efd",
                "input_background": "#4a4a4a",
                "input_border": "#666666",
                "secondary_text": "#cccccc"
            },
            "护眼主题": {
                "background": "#f0f8e8",
                "card_background": "#ffffff",
                "text_color": "#2d5016",
                "border_color": "#c8e6c9",
                "accent_color": "#4caf50",
                "hover_color": "#45a049",
                "pressed_color": "#3d8b40",
                "input_background": "#ffffff",
                "input_border": "#a5d6a7",
                "secondary_text": "#558b2f"
            },
            "温暖主题": {
                "background": "#fff8e1",
                "card_background": "#ffffff",
                "text_color": "#5d4037",
                "border_color": "#ffcc02",
                "accent_color": "#ff9800",
                "hover_color": "#f57c00",
                "pressed_color": "#ef6c00",
                "input_background": "#ffffff",
                "input_border": "#ffb74d",
                "secondary_text": "#8d6e63"
            },
            "清新主题": {
                "background": "#e3f2fd",
                "card_background": "#ffffff",
                "text_color": "#0d47a1",
                "border_color": "#90caf9",
                "accent_color": "#2196f3",
                "hover_color": "#1976d2",
                "pressed_color": "#1565c0",
                "input_background": "#ffffff",
                "input_border": "#64b5f6",
                "secondary_text": "#1976d2"
            }
        }
        self.current_theme = "默认主题"
        self.settings_file = "config/theme_settings.json"
        self.load_settings()
    
    def get_theme_names(self) -> list:
        """获取所有主题名称"""
        return list(self.themes.keys())
    
    def get_current_theme(self) -> str:
        """获取当前主题名称"""
        return self.current_theme
    
    def get_theme_colors(self, theme_name: str = None) -> Dict[str, str]:
        """获取主题颜色配置"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes["默认主题"])
    
    def set_theme(self, theme_name: str) -> bool:
        """设置当前主题"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_settings()
            return True
        return False
    
    def load_settings(self):
        """加载主题设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    theme_name = settings.get('current_theme', '默认主题')
                    if theme_name in self.themes:
                        self.current_theme = theme_name
        except Exception as e:
            print(f"加载主题设置失败: {e}")
            self.current_theme = "默认主题"
    
    def save_settings(self):
        """保存主题设置"""
        try:
            settings = {
                'current_theme': self.current_theme
            }
            # 确保config目录存在
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存主题设置失败: {e}")
    
    def generate_main_window_style(self) -> str:
        """生成主窗口样式表"""
        colors = self.get_theme_colors()
        
        return f"""
        /* 主窗口样式 */
        QMainWindow, QWidget {{
            background-color: {colors['background']};
            color: {colors['text_color']};
        }}

        /* 对话框和消息框样式 */
        QDialog, QMessageBox {{
            background-color: {colors['card_background']};
            color: {colors['text_color']};
            border-radius: 8px;
        }}

        QMessageBox{{
            background-color: {colors['card_background']};
            color: {colors['text_color']};
            border-radius: 8px;
        }}
        /* 消息框按钮样式 - 使用较低优先级，允许NMessageBox覆盖 */

        /* 消息框文本样式 */
        QMessageBox QLabel {{
            color: {colors['text_color']};
            font-size: 14px;
        }}

        /* 标题栏文本 */
        QDialog QLabel[objectName="qt_msgbox_label"] {{
            color: {colors['text_color']};
        }}

        /* 输入框通用样式 */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {colors['input_background']};
            border: 1px solid {colors['input_border']};
            border-radius: 4px;
            padding: 6px;
            color: {colors['text_color']};
            selection-background-color: {colors['accent_color']};
        }}

        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {colors['accent_color']};
        }}

        /* 按钮通用样式 */
        QPushButton {{
            background-color: #6c757d;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 2px;
            font-size: 13px;
        }}

        QPushButton:hover {{
            background-color: #5a6268;
        }}

        QPushButton:pressed {{
            background-color: #495057;
        }}

        /* 标签通用样式 */
        QLabel {{
            color: {colors['text_color']};
        }}

        /* 滚动条样式 */
        QScrollBar:vertical {{
            background-color: {colors['background']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {colors['border_color']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {colors['secondary_text']};
        }}

        /* 下拉框样式 */
        QComboBox {{
            border: 1px solid {colors['input_border']};
            border-radius: 2px;
            padding: 8px 12px;
            background-color: {colors['input_background']};
            color: {colors['text_color']};
        }}

        QComboBox:hover {{
            border-color: {colors['accent_color']};
        }}

        QComboBox QAbstractItemView {{
            border: 1px solid {colors['input_border']};
            background-color: white;
            selection-background-color: {colors['accent_color']};
            selection-color: white;
        }}
        """
    
    def generate_card_style(self) -> str:
        """生成卡片样式"""
        colors = self.get_theme_colors()
        
        return f"""
        QFrame {{
            background-color: {colors['card_background']};
            border-radius: 12px;
            border: 1px solid {colors['border_color']};
        }}
        """
    
    def generate_button_style(self, button_type: str = "primary") -> str:
        """生成按钮样式"""
        colors = self.get_theme_colors()
        
        if button_type == "primary":
            return f"""
            QPushButton {{
                background-color: {colors['accent_color']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {colors['hover_color']};
            }}
            QPushButton:pressed {{
                background-color: {colors['pressed_color']};
            }}
            """
        elif button_type == "secondary":
            return f"""
            QPushButton {{
                background-color: transparent;
                color: {colors['text_color']};
                border: 1px solid {colors['border_color']};
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {colors['border_color']};
            }}
            """
        
        return ""
