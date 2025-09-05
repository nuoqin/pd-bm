"""配置包 - 包含所有配置文件和数据文件"""

import json
import os


def load_menu_config():
    """加载菜单配置文件"""
    # 默认配置（如果JSON文件加载失败时使用）
    default_config = {
            "menu_items": [
                {
                    "text": "\uD83D\uDCBB 主页",
                    "icon": "icons/home.png",
                    "type": "normal"
                },
                {
                    "text": "\uD83D\uDCFA 密码管理",
                    "icon": "icons/flash.png",
                    "type": "normal"
                },{
                    "text": "\uD83D\uDCC2 书签管理",
                    "icon": "icons/flash.png",
                    "type": "normal"
                },{
                    "text": "\uD83D\uDCE6 书签分类",
                    "icon": "icons/flash.png",
                    "type": "normal"
                },
                {
                    "text": "设置",
                    "icon": "icons/setting.png",
                    "type": "settings"
                }
            ],
            "config": {
                "nav_width": 140,
                "button_height": 40,
                "font_family": "Microsoft YaHei",
                "font_size": 10
            }
    }
    
    return default_config
