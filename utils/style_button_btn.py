from PyQt5.QtWidgets import QAbstractButton

class StyleButtonManager:
    """样式管理器"""
    def __init__(self):
        """初始化样式管理器"""


    #设置按钮默认颜色
    @staticmethod
    def set_style_btn_sheet_default(button:QAbstractButton):
        """为按钮应用默认样式"""
        StyleButtonManager.set_style_btn_sheet(button, "#1e9fff", "white","#409eff","none")

    #设置按钮错误颜色
    @staticmethod
    def set_style_btn_sheet_error(button:QAbstractButton):
        """为按钮应用自定义样式"""
        StyleButtonManager.set_style_btn_sheet(button, "#dc3545", "white","#c82333","none")

    # 设置取消错误颜色
    @staticmethod
    def set_style_btn_sheet_cancel(button: QAbstractButton):
        """为按钮应用自定义样式"""
        StyleButtonManager.set_style_btn_sheet(button, "white", "black", "#c82333","1px solid #409eff")



    @staticmethod
    def set_style_btn_sheet(button:QAbstractButton, bg_color:str, text_color:str,hover_color:str,border_color:str):
        """为按钮应用自定义样式"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: {border_color};
                padding: 8px 12px;
                border-radius: 2px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};  
            }}
        """)


