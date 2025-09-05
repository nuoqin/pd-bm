from PyQt5.QtWidgets import QMessageBox

from utils.style import StyleButtonManager


class NMessageBox:
    """自定义样式的消息框工具类"""

    @staticmethod
    def get_theme_colors():
        """获取当前主题颜色"""
        # 尝试从主题管理器获取颜色
        try:
            from utils.theme_manager import ThemeManager
            theme_manager = ThemeManager()
            colors = theme_manager.get_theme_colors()
            return colors
        except:
            # 如果获取失败，使用默认颜色
            return {
                'card_background': '#ffffff',
                'text_color': '#333333',
                'accent_color': '#007acc',
                'hover_color': '#005a9e',
                'pressed_color': '#004080'
            }

    @staticmethod
    def apply_style(msgbox):
        """为消息框应用自定义样式"""
        colors = NMessageBox.get_theme_colors()
        msgbox.setStyleSheet(f"""
            QMessageBox {{
                background-color: {colors['card_background']};
                color: {colors['text_color']};
                border-radius: 8px;
                font-family: "Microsoft YaHei";
                min-width: 300px;
            }}

            QMessageBox QPushButton {{
                background-color: white;
                color: black !important;
                border: 1px solid red;
                padding: 10px 16px !important;
                border-radius: 2px !important;
                font-size: 12px !important;
                min-width: 80px !important;
                font-family: "Microsoft YaHei" !important;
            }}

            QMessageBox QPushButton:hover {{
                background-color: {colors['hover_color']} !important;
                border-color: {colors['hover_color']} !important;
            }}

            QMessageBox QPushButton:pressed {{
                background-color: {colors.get('pressed_color', colors['hover_color'])} !important;
                border-color: {colors.get('pressed_color', colors['hover_color'])} !important;
            }}

            QMessageBox QLabel {{
                color: {colors['text_color']};
                font-size: 12px;
                font-family: "Microsoft YaHei";
                padding: 10px;
            }}
        """)

    @staticmethod
    def information(parent, title, text):
        """显示信息消息框"""
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Information)
        # 设置按钮
        msgbox.setStandardButtons(QMessageBox.Yes)
        yes_btn = msgbox.button(QMessageBox.Yes)
        StyleButtonManager.set_style_btn_sheet_default(yes_btn)
        yes_btn.setText("确定")
        NMessageBox.apply_style(msgbox)
        return msgbox.exec_()

    @staticmethod
    def warning(parent, title, text):
        """显示警告消息框"""
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Warning)
        # 设置按钮
        yes_button = msgbox.button(QMessageBox.Yes)
        StyleButtonManager.set_style_btn_sheet_default(yes_button)
        yes_button.setText("确定")
        NMessageBox.apply_style(msgbox)
        return msgbox.exec_()

    @staticmethod
    def critical(parent, title, text):
        """显示错误消息框"""
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Critical)
        # 设置按钮
        yes_button = msgbox.button(QMessageBox.Yes)
        StyleButtonManager.set_style_btn_sheet_default(yes_button)
        yes_button.setText("确定")
        NMessageBox.apply_style(msgbox)
        return msgbox.exec_()

    @staticmethod
    def question(parent, title, text, buttons=QMessageBox.Yes | QMessageBox.No, default_button=QMessageBox.No):
        """显示问题消息框"""
        # 创建消息框
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle(title)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Question)
        # 设置按钮
        msgbox.setStandardButtons(buttons)
        yes_btn=msgbox.button(QMessageBox.Yes)
        StyleButtonManager.set_style_btn_sheet_default(yes_btn)
        yes_btn.setText("确定")
        no_btn=msgbox.button(QMessageBox.No)
        StyleButtonManager.set_style_btn_sheet_cancel(no_btn)
        no_btn.setText("取消")
        msgbox.setDefaultButton(default_button)
        NMessageBox.apply_style(msgbox)
        return msgbox.exec_()
