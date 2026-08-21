#!/usr/bin/env python3
"""
DeskMate - 跨平台桌面虚拟伴侣 / Cross-Platform Desktop Virtual Companion
主入口 / Main entry point
"""

import sys
import os

# 确保可以导入包 / Ensure package import works
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from deskmate.utils.config import ConfigManager
from deskmate.window import PetWindow
from deskmate.tray import TrayManager


def main():
    """主函数 / Main function"""
    # 高DPI支持 / High DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("DeskMate")
    app.setApplicationDisplayName("DeskMate")
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口不退出，保留托盘 / Don't quit on window close, keep tray

    # 加载配置 / Load config
    config_mgr = ConfigManager()

    # 创建宠物窗口 / Create pet window
    pet_window = PetWindow(config_mgr)
    pet_window.show()

    # 创建系统托盘 / Create system tray
    tray = TrayManager(pet_window, config_mgr)

    # 欢迎通知 / Welcome notification
    pet_name = config_mgr.config.pet_name
    tray.notify(
        "DeskMate 已启动",
        f"{pet_name} 已经来到你的桌面！\n右键宠物打开菜单，双击可以陪它玩～",
        4000
    )

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
