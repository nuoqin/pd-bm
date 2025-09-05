"""数据模型模块"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from utils.crypto_utils import SecurePasswordManager


class PasswordItem:
    """密码条目数据模型"""
    
    def __init__(self, title: str = "", description: str = "", account: str = "", password: str = "", source: str = "", item_id: str = None):
        self.id = item_id or str(int(datetime.now().timestamp() * 1000))  # 使用时间戳作为ID
        self.title = title
        self.source = source
        self.description = description
        self.account = account
        self.password = password
        self.created_time = datetime.now().isoformat()
        self.updated_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'source': self.source,
            'description': self.description,
            'account': self.account,
            'password': self.password,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordItem':
        """从字典创建实例"""
        item = cls(
            title=data.get('title', ''),
            source=data.get('source', ''),
            description=data.get('description', ''),
            account=data.get('account', ''),
            password=data.get('password', ''),
            item_id=data.get('id')
        )
        item.created_time = data.get('created_time', item.created_time)
        item.updated_time = data.get('updated_time', item.updated_time)
        return item
    
    def update(self, title: str = None, source: str = None, description: str = None, account: str = None, password: str = None):
        """更新数据"""
        if title is not None:
            self.title = title
        if source is not None:
            self.source = source
        if description is not None:
            self.description = description
        if account is not None:
            self.account = account
        if password is not None:
            self.password = password
        self.updated_time = datetime.now().isoformat()


class BookmarkItem:
    """书签条目数据模型"""
    
    def __init__(self, title: str = "", description: str = "", url: str = "", category: str = "默认分类", item_id: str = None):
        self.id = item_id or str(int(datetime.now().timestamp() * 1000))  # 使用时间戳作为ID
        self.title = title
        self.url = url
        self.description = description
        self.category = category
        self.created_time = datetime.now().isoformat()
        self.updated_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'category': self.category,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BookmarkItem':
        """从字典创建实例"""
        item = cls(
            title=data.get('title', ''),
            url=data.get('url', ''),
            description=data.get('description', ''),
            category=data.get('category', '默认分类'),
            item_id=data.get('id')
        )
        item.created_time = data.get('created_time', item.created_time)
        item.updated_time = data.get('updated_time', item.updated_time)
        return item
    
    def update(self, title: str = None, url: str = None, description: str = None, category: str = None):
        """更新数据"""
        if title is not None:
            self.title = title
        if url is not None:
            self.url = url
        if description is not None:
            self.description = description
        if category is not None:
            self.category = category
        self.updated_time = datetime.now().isoformat()


class PasswordManager:
    """密码管理器"""
    def __init__(self, data_file: str = "config/passwords.json", encrypted_file: str = "config/passwords.enc"):
        self.data_file = data_file
        self.encrypted_file = encrypted_file
        self.passwords: List[PasswordItem] = []
        self.secure_manager = SecurePasswordManager(data_file, encrypted_file)
        self.encryption_key = None
        self.use_encryption = False
    
    def set_encryption_key(self, key: str):
        """设置加密密钥"""
        self.encryption_key = key
        self.secure_manager.set_encryption_key(key, use_simple_key=True)  # 使用简单密钥派生
        self.use_encryption = True

    def load_data(self):
        """从文件加载数据"""
        try:
            if self.use_encryption and os.path.exists(self.encrypted_file):
                # 加载加密数据
                try:
                    data = self.secure_manager.load_encrypted_data()
                    self.passwords = [PasswordItem.from_dict(item) for item in data]
                    print(f"从加密文件加载了 {len(self.passwords)} 个密码条目")
                except Exception as decrypt_error:
                    # 解密失败，可能是密码错误
                    print(f"解密失败，可能是访问密码错误: {decrypt_error}")
                    raise Exception("访问密码错误，无法解密数据！请确认输入的访问密码是否正确。")
            elif os.path.exists(self.data_file):
                # 加载明文数据
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.passwords = [PasswordItem.from_dict(item) for item in data]

                # 如果启用了加密，自动迁移到加密存储
                if self.use_encryption and data:
                    print(f"检测到明文数据，自动迁移到加密存储...")
                    self.secure_manager.migrate_to_encrypted(data)
                    print("数据迁移完成")

                print(f"从明文文件加载了 {len(self.passwords)} 个密码条目")
            else:
                self.passwords = []
                print("未找到密码数据文件")
        except Exception as e:
            if "访问密码错误" in str(e):
                # 重新抛出密码错误，不要设置为空列表
                raise e
            else:
                print(f"加载密码数据失败: {e}")
                self.passwords = []
    
    def save_data(self):
        """保存数据到文件"""
        try:
            print(f"开始保存密码数据，共 {len(self.passwords)} 个条目")
            data = [password.to_dict() for password in self.passwords]

            if self.use_encryption:
                # 保存为加密数据
                print("使用加密模式保存数据...")
                self.secure_manager.save_encrypted_data(data)
                print(f"已加密保存 {len(self.passwords)} 个密码条目")
            else:
                # 保存为明文数据
                print("使用明文模式保存数据...")
                # 确保config目录存在
                os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"已明文保存 {len(self.passwords)} 个密码条目")
            print("密码数据保存完成")
        except Exception as e:
            print(f"保存密码数据失败: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"保存密码数据失败: {e}")
    
    def add_password(self, title: str, source: str, description: str, account: str, password: str) -> PasswordItem:
        """添加新密码"""
        item = PasswordItem(title, description, account, password, source)
        self.passwords.insert(0,item)
        self.save_data()
        return item
    
    def update_password(self, item_id: str, title: str = None, source: str = None, description: str = None, 
                       account: str = None, password: str = None) -> bool:
        """更新密码"""
        for item in self.passwords:
            if item.id == item_id:
                item.update(title, source, description, account, password)
                self.save_data()
                return True
        return False
    
    def delete_password(self, item_id: str) -> bool:
        """删除密码"""
        for i, item in enumerate(self.passwords):
            if item.id == item_id:
                del self.passwords[i]
                self.save_data()
                return True
        return False
    
    def search_passwords(self, query: str) -> List[PasswordItem]:
        """搜索密码"""
        if not query:
            return self.passwords
        
        query = query.lower()
        results = []
        for item in self.passwords:
            if (query in item.title.lower() or 
                query in item.source.lower() or
                query in item.description.lower() or 
                query in item.account.lower()):
                results.append(item)
        return results
    
    def get_all_passwords(self) -> List[PasswordItem]:
        """获取所有密码"""
        return self.passwords
    
    def get_password_by_id(self, item_id: str) -> Optional[PasswordItem]:
        """根据ID获取密码"""
        for item in self.passwords:
            if item.id == item_id:
                return item
        return None


class BookmarkManager:
    """书签管理器"""

    def __init__(self, data_file: str = "config/bookmarks.json", encrypted_file: str = "config/bookmarks.enc"):
        self.data_file = data_file
        self.encrypted_file = encrypted_file
        self.bookmarks: List[BookmarkItem] = []
        self.secure_manager = SecurePasswordManager(data_file, encrypted_file)
        self.encryption_key = None
        self.use_encryption = False

    def set_encryption_key(self, key: str):
        """设置加密密钥"""
        self.encryption_key = key
        self.secure_manager.set_encryption_key(key, use_simple_key=True)  # 使用简单密钥派生
        self.use_encryption = True

    def load_data(self):
        """从文件加载数据"""
        try:
            if self.use_encryption and os.path.exists(self.encrypted_file):
                # 加载加密数据
                try:
                    data = self.secure_manager.load_encrypted_data()
                    self.bookmarks = [BookmarkItem.from_dict(item) for item in data]
                    print(f"从加密文件加载了 {len(self.bookmarks)} 个书签条目")
                except Exception as decrypt_error:
                    # 解密失败，可能是密码错误
                    print(f"解密失败，可能是访问密码错误: {decrypt_error}")
                    raise Exception("访问密码错误，无法解密数据！请确认输入的访问密码是否正确。")
            elif os.path.exists(self.data_file):
                # 加载明文数据
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.bookmarks = [BookmarkItem.from_dict(item) for item in data]

                # 如果启用了加密，自动迁移到加密存储
                if self.use_encryption and data:
                    print(f"检测到明文数据，自动迁移到加密存储...")
                    self.secure_manager.migrate_to_encrypted(data)
                    print("数据迁移完成")

                print(f"从明文文件加载了 {len(self.bookmarks)} 个书签条目")
            else:
                self.bookmarks = []
                print("未找到书签数据文件")
        except Exception as e:
            if "访问密码错误" in str(e):
                # 重新抛出密码错误，不要设置为空列表
                raise e
            else:
                print(f"加载书签数据失败: {e}")
                self.bookmarks = []

    def save_data(self):
        """保存数据到文件"""
        try:
            print(f"开始保存书签数据，共 {len(self.bookmarks)} 个条目")
            data = [bookmark.to_dict() for bookmark in self.bookmarks]

            if self.use_encryption:
                # 保存为加密数据
                print("使用加密模式保存数据...")
                self.secure_manager.save_encrypted_data(data)
                print(f"已加密保存 {len(self.bookmarks)} 个书签条目")
            else:
                # 保存为明文数据
                print("使用明文模式保存数据...")
                # 确保config目录存在
                os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"已明文保存 {len(self.bookmarks)} 个书签条目")
            print("书签数据保存完成")
        except Exception as e:
            print(f"保存书签数据失败: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"保存书签数据失败: {e}")

    def add_bookmark(self, title: str, url: str, description: str, category: str = "默认分类") -> BookmarkItem:
        """添加新书签"""
        item = BookmarkItem(title, description, url, category)
        self.bookmarks.insert(0,item)
        self.save_data()
        return item

    def update_bookmark(self, item_id: str, title: str = None, url: str = None, description: str = None, category: str = None) -> bool:
        """更新书签"""
        for item in self.bookmarks:
            if item.id == item_id:
                item.update(title, url, description, category)
                self.save_data()
                return True
        return False

    def delete_bookmark(self, item_id: str) -> bool:
        """删除书签"""
        for i, item in enumerate(self.bookmarks):
            if item.id == item_id:
                del self.bookmarks[i]
                self.save_data()
                return True
        return False

    def search_bookmarks(self, query: str) -> List[BookmarkItem]:
        """搜索书签"""
        if not query:
            return self.bookmarks

        query = query.lower()
        results = []
        for item in self.bookmarks:
            if (query in item.title.lower() or 
                query in item.url.lower() or
                query in item.description.lower() or
                query in item.category.lower()):
                results.append(item)
        return results

    def get_all_bookmarks(self) -> List[BookmarkItem]:
        """获取所有书签"""
        return self.bookmarks

    def get_bookmark_by_id(self, item_id: str) -> Optional[BookmarkItem]:
        """根据ID获取书签"""
        for item in self.bookmarks:
            if item.id == item_id:
                return item
        return None

    def get_bookmarks_by_category(self, category: str) -> List[BookmarkItem]:
        """根据分类获取书签"""
        return [item for item in self.bookmarks if item.category == category]

    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set()
        for item in self.bookmarks:
            categories.add(item.category)
        return sorted(list(categories))

    def get_bookmarks_grouped_by_category(self) -> Dict[str, List[BookmarkItem]]:
        """获取按分类分组的书签"""
        grouped = {}
        for item in self.bookmarks:
            if item.category not in grouped:
                grouped[item.category] = []
            grouped[item.category].append(item)
        return grouped


class BookmarkCategory:
    """书签分类数据模型"""
    
    def __init__(self, name: str = "", description: str = "", color: str = "#007acc", item_id: str = None):
        self.id = item_id or str(int(datetime.now().timestamp() * 1000))
        self.name = name
        self.description = description
        self.color = color
        self.created_time = datetime.now().isoformat()
        self.updated_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BookmarkCategory':
        """从字典创建实例"""
        item = cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            color=data.get('color', '#007acc'),
            item_id=data.get('id')
        )
        item.created_time = data.get('created_time', item.created_time)
        item.updated_time = data.get('updated_time', item.updated_time)
        return item
    
    def update(self, name: str = None, description: str = None, color: str = None):
        """更新数据"""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if color is not None:
            self.color = color
        self.updated_time = datetime.now().isoformat()


class BookmarkCategoryManager:
    """书签分类管理器"""

    def __init__(self, data_file: str = "config/bookmark_categories.json", encrypted_file: str = "config/bookmark_categories.enc"):
        self.data_file = data_file
        self.encrypted_file = encrypted_file
        self.categories: List[BookmarkCategory] = []
        self.secure_manager = SecurePasswordManager(data_file, encrypted_file)
        self.encryption_key = None
        self.use_encryption = False
        
        # 初始化默认分类
        self.init_default_categories()

    def init_default_categories(self):
        """初始化默认分类"""
        default_categories = [
            {"name": "默认分类", "description": "默认书签分类", "color": "#007acc"},
            {"name": "工作学习", "description": "工作和学习相关的书签", "color": "#28a745"},
            {"name": "娱乐休闲", "description": "娱乐和休闲相关的书签", "color": "#dc3545"},
            {"name": "工具软件", "description": "实用工具和软件相关的书签", "color": "#ffc107"},
            {"name": "技术开发", "description": "编程和技术开发相关的书签", "color": "#6f42c1"}
        ]
        
        for cat_data in default_categories:
            category = BookmarkCategory(
                name=cat_data["name"],
                description=cat_data["description"],
                color=cat_data["color"]
            )
            self.categories.append(category)

    def set_encryption_key(self, key: str):
        """设置加密密钥"""
        self.encryption_key = key
        self.secure_manager.set_encryption_key(key, use_simple_key=True)
        self.use_encryption = True

    def load_data(self):
        """从文件加载数据"""
        try:
            if self.use_encryption and os.path.exists(self.encrypted_file):
                # 加载加密数据
                try:
                    data = self.secure_manager.load_encrypted_data()
                    self.categories = [BookmarkCategory.from_dict(item) for item in data]
                    print(f"从加密文件加载了 {len(self.categories)} 个分类")
                except Exception as decrypt_error:
                    print(f"解密失败，可能是访问密码错误: {decrypt_error}")
                    raise Exception("访问密码错误，无法解密数据！请确认输入的访问密码是否正确。")
            elif os.path.exists(self.data_file):
                # 加载明文数据
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.categories = [BookmarkCategory.from_dict(item) for item in data]

                # 如果启用了加密，自动迁移到加密存储
                if self.use_encryption and data:
                    print(f"检测到明文数据，自动迁移到加密存储...")
                    self.secure_manager.migrate_to_encrypted(data)
                    print("数据迁移完成")

                print(f"从明文文件加载了 {len(self.categories)} 个分类")
            else:
                # 如果没有数据文件，保存默认分类
                self.save_data()
                print("创建了默认分类")
        except Exception as e:
            if "访问密码错误" in str(e):
                raise e
            else:
                print(f"加载分类数据失败: {e}")
                # 保持默认分类
                self.init_default_categories()

    def save_data(self):
        """保存数据到文件"""
        try:
            data = [category.to_dict() for category in self.categories]

            if self.use_encryption:
                # 保存为加密数据
                self.secure_manager.save_encrypted_data(data)
                print(f"已加密保存 {len(self.categories)} 个分类")
            else:
                # 保存为明文数据
                os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"已明文保存 {len(self.categories)} 个分类")
        except Exception as e:
            print(f"保存分类数据失败: {e}")

    def add_category(self, name: str, description: str = "", color: str = "#007acc") -> BookmarkCategory:
        """添加新分类"""
        # 检查分类名是否已存在
        for category in self.categories:
            if category.name == name:
                raise ValueError(f"分类 '{name}' 已存在")
        
        item = BookmarkCategory(name, description, color)
        self.categories.insert(0,item)
        self.save_data()
        return item

    def update_category(self, item_id: str, name: str = None, description: str = None, color: str = None) -> bool:
        """更新分类"""
        # 如果要更新名称，检查是否与其他分类重名
        if name is not None:
            for category in self.categories:
                if category.id != item_id and category.name == name:
                    raise ValueError(f"分类 '{name}' 已存在")
        
        for item in self.categories:
            if item.id == item_id:
                item.update(name, description, color)
                self.save_data()
                return True
        return False

    def delete_category(self, item_id: str) -> bool:
        """删除分类"""
        # 不允许删除默认分类
        category_to_delete = None
        for item in self.categories:
            if item.id == item_id:
                if item.name == "默认分类":
                    raise ValueError("不能删除默认分类")
                category_to_delete = item
                break
        
        if not category_to_delete:
            return False
        
        # 删除分类
        for i, item in enumerate(self.categories):
            if item.id == item_id:
                del self.categories[i]
                self.save_data()
                return True
        return False

    def get_all_categories(self) -> List[BookmarkCategory]:
        """获取所有分类"""
        return self.categories

    def get_category_by_id(self, item_id: str) -> Optional[BookmarkCategory]:
        """根据ID获取分类"""
        for item in self.categories:
            if item.id == item_id:
                return item
        return None

    def get_category_by_name(self, name: str) -> Optional[BookmarkCategory]:
        """根据名称获取分类"""
        for item in self.categories:
            if item.name == name:
                return item
        return None

    def get_category_names(self) -> List[str]:
        """获取所有分类名称"""
        return [category.name for category in self.categories]
