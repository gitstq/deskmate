"""
系统托盘集成 / System tray integration
提供托盘图标、菜单、通知功能 / Provides tray icon, menu, and notification functionality
"""

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt

from .pets import PET_DISPLAY_NAMES


class TrayManager:
    """
    系统托盘管理器 / System tray manager
    """

    def __init__(self, pet_window, config_manager):
        self.pet_window = pet_window
        self.config_mgr = config_manager
        self.tray = QSystemTrayIcon(pet_window)
        self._setup_tray()

    def _create_icon(self) -> QIcon:
        """程序化生成托盘图标 / Programmatically generate tray icon"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # 圆形背景 / Circle background
        painter.setBrush(QBrush(QColor("#FF6B9D")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(4, 4, 56, 56)

        # 简单爪印 / Simple paw print
        painter.setBrush(QBrush(QColor("white")))
        # 大垫 / Main pad
        painter.drawEllipse(22, 34, 20, 16)
        # 四个脚趾 / Four toes
        painter.drawEllipse(14, 22, 10, 10)
        painter.drawEllipse(27, 16, 10, 10)
        painter.drawEllipse(40, 22, 10, 10)
        painter.drawEllipse(48, 30, 8, 8)

        painter.end()
        return QIcon(pixmap)

    def _setup_tray(self):
        """配置托盘 / Configure tray"""
        icon = self._create_icon()
        self.tray.setIcon(icon)
        self.tray.setToolTip("DeskMate - 你的桌面伴侣")

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(40, 40, 50, 230);
                color: white;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: rgba(100, 120, 255, 0.6);
            }
            QMenu::separator {
                height: 1px;
                background: rgba(255,255,255,0.15);
                margin: 4px 8px;
            }
        """)

        # 显示/隐藏 / Show/Hide
        toggle_action = QAction("👁️ 显示/隐藏宠物", self.tray)
        toggle_action.triggered.connect(self._toggle_visibility)
        menu.addAction(toggle_action)

        menu.addSeparator()

        # 宠物切换 / Pet switch
        pet_menu = menu.addMenu("🐾 切换宠物")
        for species, display in PET_DISPLAY_NAMES.items():
            action = QAction(display, self.tray)
            action.triggered.connect(lambda checked, s=species: self.pet_window._switch_pet(s))
            pet_menu.addAction(action)

        menu.addSeparator()

        # 番茄钟 / Pomodoro
        pomo_start = QAction("🍅 开始专注", self.tray)
        pomo_start.triggered.connect(self.pet_window.pomodoro.start)
        menu.addAction(pomo_start)

        pomo_stop = QAction("⏹️ 停止专注", self.tray)
        pomo_stop.triggered.connect(self.pet_window.pomodoro.stop)
        menu.addAction(pomo_stop)

        menu.addSeparator()

        # 关于 / About
        about_action = QAction("ℹ️ 关于 DeskMate", self.tray)
        about_action.triggered.connect(self._show_about)
        menu.addAction(about_action)

        menu.addSeparator()

        # 退出 / Quit
        quit_action = QAction("❌ 退出", self.tray)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _toggle_visibility(self):
        """切换显示/隐藏 / Toggle visibility"""
        if self.pet_window.isVisible():
            self.pet_window.hide()
        else:
            self.pet_window.show()

    def _on_tray_activated(self, reason):
        """托盘点击事件 / Tray click event"""
        if reason == QSystemTrayIcon.Trigger:  # 左键单击 / Left click
            self._toggle_visibility()
        elif reason == QSystemTrayIcon.DoubleClick:  # 双击 / Double click
            self.pet_window.show()
            self.pet_window.raise_()
            self.pet_window.activateWindow()

    def _show_about(self):
        """显示关于信息 / Show about info via notification"""
        self.tray.showMessage(
            "DeskMate v1.0.0",
            "跨平台桌面虚拟伴侣\n"
            "支持猫/狗/兔/狐四种角色\n"
            "内置番茄钟与系统监控\n"
            "MIT 开源协议",
            QSystemTrayIcon.Information,
            5000
        )

    def notify(self, title: str, message: str, duration: int = 5000):
        """发送系统通知 / Send system notification"""
        self.tray.showMessage(title, message, QSystemTrayIcon.Information, duration)
