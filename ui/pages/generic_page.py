"""通用页面模块"""

from .base_page import BasePage


class GenericPage(BasePage):
    """通用功能页面"""
    
    def __init__(self, title):
        super().__init__(title)
    
    def init_ui(self):
        """初始化通用界面"""
        # 功能标题卡片
        title_card = self.create_card(f"{self.title}功能界面", bold=True, size=16)
        self.add_card(title_card)
        
        # 说明卡片
        desc_card = self.create_card(f"这里是{self.title}的功能界面，您可以在这里添加具体的功能实现。")
        self.add_card(desc_card)
        
        self.add_stretch()
