"""AES加密解密工具模块"""

import base64
import hashlib
import json
from typing import Dict, List, Any
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class CryptoAesUtils:

    @staticmethod
    def generate_key_from_password(password: str) -> str:
        """根据用户输入的密码生成AES密钥"""
        # 使用SHA256生成32字节密钥
        key_hash = hashlib.sha256(password.encode('utf-8')).digest()
        return key_hash.hex()


    """AES加密解密工具类"""
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """从密码派生AES密钥"""
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))
        return key, salt

    @staticmethod
    def derive_key_simple(password: str) -> bytes:
        """简单地从密码派生AES密钥（用于用户自定义密码）"""
        key_hash = hashlib.sha256(password.encode('utf-8')).digest()
        return key_hash

    @staticmethod
    def encrypt_data(data: str, key: str, use_simple_key: bool = False) -> Dict[str, str]:
        """加密数据"""
        try:
            if use_simple_key:
                key_bytes = CryptoAesUtils.derive_key_simple(key)
                salt = b''
            else:
                key_bytes, salt = CryptoAesUtils.derive_key(key)

            # 生成随机IV
            iv = os.urandom(16)
            # 创建AES加密器
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            # 准备数据进行加密
            data_bytes = data.encode('utf-8')
            block_size = 16
            padding_length = block_size - (len(data_bytes) % block_size)
            padded_data = data_bytes + bytes([padding_length]) * padding_length
            # 加密数据
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            # 返回包含salt、iv和加密数据的字典
            return {
                'salt': base64.b64encode(salt).decode('utf-8') if salt else '',
                'iv': base64.b64encode(iv).decode('utf-8'),
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'use_simple_key': str(use_simple_key)
            }
        except Exception as e:
            raise Exception(f"加密失败: {str(e)}")

    @staticmethod
    def decrypt_data(encrypted_dict: Dict[str, str], key: str) -> str:
        """解密数据"""
        try:
            # 解码base64数据
            salt = base64.b64decode(encrypted_dict.get('salt', '')) if encrypted_dict.get('salt') else b''
            iv = base64.b64decode(encrypted_dict['iv'])
            encrypted_data = base64.b64decode(encrypted_dict['data'])
            use_simple_key = encrypted_dict.get('use_simple_key', 'False') == 'True'

            if use_simple_key:
                # 使用简单的密钥派生
                key_bytes = CryptoAesUtils.derive_key_simple(key)
            else:
                # 使用PBKDF2派生
                key_bytes, _ = CryptoAesUtils.derive_key(key, salt) if salt else CryptoUtils.derive_key(key)

            # 创建AES解密器
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
            decrypt = cipher.decryptor()

            # 解密数据
            decrypted_padded = decrypt.update(encrypted_data) + decrypt.finalize()

            # 移除填充
            padding_length = decrypted_padded[-1]
            if padding_length > 16:
                raise Exception("无效的填充")
            decrypted_data = decrypted_padded[:-padding_length]

            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise Exception(f"解密失败: {str(e)}")

    @staticmethod
    def encrypt_json_data(data: Any, key: str, use_simple_key: bool = False) -> Dict[str, str]:
        """加密JSON数据"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return CryptoAesUtils.encrypt_data(json_str, key, use_simple_key)

    @staticmethod
    def decrypt_json_data(encrypted_dict: Dict[str, str], key: str) -> Any:
        """解密JSON数据"""
        json_str = CryptoAesUtils.decrypt_data(encrypted_dict, key)
        return json.loads(json_str)


class SecurePasswordManager:
    """安全的密码管理器"""
    def __init__(self, data_file: str = "config/passwords.json", encrypted_file: str = "config/passwords.enc"):
        self.data_file = data_file
        self.encrypted_file = encrypted_file
        self.encryption_key = None
        self.is_encrypted = False
        self.use_simple_key = False

    def set_encryption_key(self, key: str, use_simple_key: bool = False):
        """设置加密密钥"""
        self.encryption_key = key
        self.use_simple_key = use_simple_key

    def load_encrypted_data(self) -> List[Dict]:
        """加载加密的数据"""
        if not self.encryption_key:
            raise Exception("未设置加密密钥")

        try:
            if os.path.exists(self.encrypted_file):
                with open(self.encrypted_file, 'r', encoding='utf-8') as f:
                    encrypted_dict = json.load(f)

                return CryptoAesUtils.decrypt_json_data(encrypted_dict, self.encryption_key)
            else:
                return []
        except Exception as e:
            raise Exception(f"加载加密数据失败: {str(e)}")

    def save_encrypted_data(self, data: List[Dict]):
        """保存加密的数据"""
        if not self.encryption_key:
            raise Exception("未设置加密密钥")

        try:
            print(f"开始加密数据，共 {len(data)} 个条目")
            encrypted_dict = CryptoAesUtils.encrypt_json_data(data, self.encryption_key, self.use_simple_key)
            print("数据加密完成")

            # 确保config目录存在
            config_dir = os.path.dirname(self.encrypted_file)
            if config_dir:
                os.makedirs(config_dir, exist_ok=True)
                print(f"确保目录存在: {config_dir}")

            print(f"准备写入文件: {self.encrypted_file}")
            with open(self.encrypted_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_dict, f, ensure_ascii=False, indent=2)
            print("加密文件写入完成")

            self.is_encrypted = True
        except Exception as e:
            print(f"保存加密数据时发生异常: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"保存加密数据失败: {str(e)}")

    def migrate_to_encrypted(self, data: List[Dict]):
        """从明文迁移到加密存储"""
        if not self.encryption_key:
            raise Exception("未设置加密密钥")

        # 保存加密数据
        self.save_encrypted_data(data)
        # 删除明文文件（可选）
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def migrate_to_plaintext(self, data: List[Dict]):
        """从加密迁移到明文存储"""
        try:
            # 保存明文数据
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # 删除加密文件
            if os.path.exists(self.encrypted_file):
                os.remove(self.encrypted_file)

            self.is_encrypted = False
        except Exception as e:
            raise Exception(f"迁移到明文失败: {str(e)}")
