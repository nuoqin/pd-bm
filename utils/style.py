from PyQt5.QtWidgets import QAbstractButton, QComboBox, QLineEdit


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


class StyleQComboBoxManager:

    def __init__(self):
        """初始化样式管理器"""

    @staticmethod
    def set_style_comboBox_default(qComboBox: QComboBox):
        """为按钮应用自定义样式"""
        qComboBox.setStyleSheet("""
                QComboBox {
                    combobox-popup: 0;
                    padding: 4px 12px;
                    height: 22px;
                    border-radius: 2px;
                    font-size: 14px;
                    font-weight: 400;
                    color: rgba(93,169,255,1);
                    line-height: 22px;
                }
                QComboBox:hover {
                    border-color: #007acc;
                }
                QComboBox::drop-down {
                    border: none;
                    height: 30px;
                    line-height: 22px;
                }
                QComboBox::down-arrow {
                    image: none;
                    height: 30px;
                    margin-right: 5px;
                }
                QComboBox QAbstractItemView {
                    border: none;
                    background-color: white;
                    selection-background-color: #007acc;
                    selection-color: white;
                }
            """)


class StyleQLineEditManager:

    def __init__(self):
        """初始化样式管理器"""

    @staticmethod
    def set_style_edit_default(qLineEdit: QLineEdit):
        """为按钮应用自定义样式"""
        qLineEdit.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ced4da; 
                    border-radius: 2px; 
                    padding: 6px 12px;
                    font-size: 12px;
                }
                
                QLineEdit:focus {
                    border-color: #007acc;
                    outline: none;
                }
            """)

    @staticmethod
    def set_style_search_default(qLineEdit: QLineEdit):
        """为按钮应用自定义样式"""
        qLineEdit.setStyleSheet("""
           QLineEdit {
                padding: 5px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 2px;
                font-size: 14px;
                height: 24px;
                background-color: #ffffff;
                color: #333333;
            }
            QLineEdit:focus {
                border-color: #007acc;
                outline: none;
            }
        """)