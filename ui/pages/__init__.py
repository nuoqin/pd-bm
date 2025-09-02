"""页面模块 - 包含所有页面类的定义"""

from .base_page import BasePage
from .home_page import HomePage  
from .password_page import PasswordManagerPage
from .bookmark_page import BookmarkManagerPage
from .bookmark_category_page import BookmarkCategoryManagerPage
from .settings_page import SettingsPage
from .generic_page import GenericPage

__all__ = [
    'BasePage',
    'HomePage', 
    'PasswordManagerPage',
    'BookmarkManagerPage',
    'BookmarkCategoryManagerPage',
    'SettingsPage',
    'GenericPage'
]
