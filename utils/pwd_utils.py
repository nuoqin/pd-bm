"""修改验证码"""
from model import PasswordManager, BookmarkManager, BookmarkCategoryManager
from utils import NMessageBox
from utils.crypto_utils import CryptoAesUtils


class PasswordOperate:
    def __init__(self, key: str):
        """验证码修改"""
        #密码管理
        self.pwm=PasswordManager()
        self.pwm.set_encryption_key(key)
        #书签
        self.bi=BookmarkManager()
        self.bi.set_encryption_key(key)
        #书签分类
        self.bic=BookmarkCategoryManager()
        self.bic.set_encryption_key(key)
        self.key=key

    def changePwd(self,oldKey,newKey,resetKey):
        #得到加密key
        oldKey=CryptoAesUtils.generate_key_from_password(oldKey)
        if not self.key == oldKey:
            NMessageBox.critical(None,"修改访问码","旧访问码输入错误！")

        if not newKey== resetKey:
            NMessageBox.critical(None,"修改访问码","两次输入的新访问码不一致！")
        #处理密码管理
        self.handler_password_manager(newKey)
        self.handler_bookmarker_manager(newKey)
        self.handler_bookmarker_category_manager(newKey)
        NMessageBox.information(None, "修改访问码", "访问码修改成功！请重启系统。")
        #停止3秒。重启


    """
    密码管理修改
    """
    def handler_password_manager(self,newKey):
        # 加载所有的data
        self.pwm.load_data()
        #重设key
        newKey=CryptoAesUtils.generate_key_from_password(newKey)
        self.pwm.set_encryption_key(newKey)
        self.pwm.save_data()

    """
    书签
    """
    def handler_bookmarker_manager(self,newKey):
        # 加载所有的data
        self.bi.load_data()
        # 重设key
        newKey = CryptoAesUtils.generate_key_from_password(newKey)
        self.bi.set_encryption_key(newKey)
        self.bi.save_data()

    """
    书签分类
    """
    def handler_bookmarker_category_manager(self,newKey):
        # 加载所有的data
        self.bic.load_data()
        # 重设key
        newKey = CryptoAesUtils.generate_key_from_password(newKey)
        self.bic.set_encryption_key(newKey)
        self.bic.save_data()