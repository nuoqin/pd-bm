# 🔐 nuoqin管理平台

一个本地化管理工具，专注于为用户提供安全、便捷的密码和书签数据管理体验。

## ✨ 功能特性

- 🔑 **密码管理**: 安全存储和管理各类账户信息
- 🔖 **书签管理**: 收藏和分类整理网站链接  
- 🛡️ **AES加密**: 采用AES加密技术保护数据安全
- 📱 **现代化UI**: 基于PyQt5的现代化用户界面
- 🎨 **主题切换**: 支持多种界面主题
- 🏠 **本地存储**: 数据完全本地化，隐私完全由您掌控

## 🚀 快速开始

### 方式一：运行源码
```bash
# 克隆项目
git clone https://github.com/nuoqin/nuoqin-manager.git
cd nuoqin-manager

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
```

## 📦 打包说明

### 环境要求
- Python 3.10+
- PyQt5 >= 5.15.0
- cryptography >= 3.4.0
- PyInstaller (用于打包)

### 打包步骤

#### Windows用户
```bash
pyinstaller -F -w -i tools.ico --name="nuoqin" main.py --add-data "ui;ui" --add-data "utils;utils" --add-data "model;model"
```

## 🛠️ 技术栈
- **GUI框架**: PyQt5
- **加密库**: cryptography (AES加密)
- **打包工具**: PyInstaller
- **开发语言**: Python 3.x


## 📝 更新日志

### v1.0.0
- ✅ 实现密码管理功能
- ✅ 实现书签管理功能
- ✅ 添加AES加密支持
- ✅ 实现主题切换功能
- ✅ 完成PyInstaller打包配置

## 🤝 贡献指南

欢迎提交Issue和Pull Request！


## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👨‍💻 作者

**nuoqin**
- GitHub: [@nuoqin](https://github.com/nuoqin)

## 🌟 支持项目

如果这个项目对您有帮助，请给个Star⭐支持一下！

---

感谢您使用nuoqin管理平台！