"""
桌面宠物窗口 / Desktop pet window
透明、无边框、始终置顶的桌面层 / Transparent, frameless, always-on-top desktop layer
"""

from PyQt5.QtWidgets import QWidget, QMenu, QAction, QApplication, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QPoint, QRectF, pyqtSignal

from .pet import BasePet, PetState
from .pets import create_pet, PET_REGISTRY, PET_DISPLAY_NAMES
from .utils.config import ConfigManager
from .utils.pomodoro import PomodoroTimer, PomodoroState
from .utils.system_monitor import SystemMonitor


class PetWindow(QWidget):
    """
    桌面宠物主窗口 / Main desktop pet window
    """

    # 信号 / Signals
    pet_changed = pyqtSignal(str)

    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_mgr = config_manager
        self.cfg = config_manager.config

        # 创建宠物 / Create pet
        self.pet = create_pet(self.cfg.pet_species, self.cfg.pet_name)
        self.pet.on_speak = self._on_pet_speak

        # 番茄钟 / Pomodoro
        self.pomodoro = PomodoroTimer(
            self.cfg.pomodoro_work_minutes,
            self.cfg.pomodoro_break_minutes
        )
        self.pomodoro.on_work_complete = self._on_work_complete
        self.pomodoro.on_break_start = self._on_break_start
        self.pomodoro.on_break_complete = self._on_break_complete

        # 系统监控 / System monitor
        self.sys_monitor = SystemMonitor()

        # 窗口设置 / Window setup
        self._setup_window()

        # 拖拽 / Dragging
        self._dragging = False
        self._drag_offset = QPoint()

        # 动画定时器 / Animation timer
        self._frame_time = 16  # ~60fps
        self._last_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_tick)
        self.timer.start(self._frame_time)

        # 对话气泡 / Speech bubble
        self._speech_text = ""
        self._speech_timer = QTimer(self)
        self._speech_timer.setSingleShot(True)
        self._speech_timer.timeout.connect(self._clear_speech)

        # 右键菜单 / Context menu
        self._build_context_menu()

        # 初始位置 / Initial position
        self._position_initial()

    def _setup_window(self):
        """配置窗口属性 / Configure window properties"""
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setMouseTracking(True)

        # 初始大小 / Initial size
        self.resize(200, 200)

    def _position_initial(self):
        """初始位置：屏幕右下角 / Initial position: bottom-right of screen"""
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 50
        y = screen.height() - self.height() - 100
        self.move(x, y)
        self.pet.x = self.width() / 2
        self.pet.y = self.height() / 2 + 10

    def _build_context_menu(self):
        """构建右键菜单 / Build context menu"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _show_context_menu(self, pos):
        """显示右键菜单 / Show context menu"""
        menu = QMenu(self)
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

        # 宠物切换 / Pet switch submenu
        pet_menu = menu.addMenu("🐾 切换宠物 / Switch Pet")
        for species, display in PET_DISPLAY_NAMES.items():
            action = QAction(display, self)
            action.triggered.connect(lambda checked, s=species: self._switch_pet(s))
            pet_menu.addAction(action)

        menu.addSeparator()

        # 交互 / Interactions
        feed_action = QAction("🍖 喂食 / Feed", self)
        feed_action.triggered.connect(self.pet.feed)
        menu.addAction(feed_action)

        play_action = QAction("🎾 玩耍 / Play", self)
        play_action.triggered.connect(self.pet.play)
        menu.addAction(play_action)

        pet_action = QAction("🤚 抚摸 / Pet", self)
        pet_action.triggered.connect(self.pet.pet)
        menu.addAction(pet_action)

        sleep_action = QAction("😴 睡觉 / Sleep", self)
        sleep_action.triggered.connect(self.pet.sleep)
        menu.addAction(sleep_action)

        clean_action = QAction("🧼 清洁 / Clean", self)
        clean_action.triggered.connect(self.pet.clean)
        menu.addAction(clean_action)

        menu.addSeparator()

        # 番茄钟 / Pomodoro
        if self.cfg.enable_pomodoro:
            if self.pomodoro.state in (PomodoroState.IDLE,):
                pomo_action = QAction("🍅 开始专注 / Start Focus", self)
                pomo_action.triggered.connect(self.pomodoro.start)
            elif self.pomodoro.state == PomodoroState.PAUSED:
                pomo_action = QAction("▶️ 继续 / Resume", self)
                pomo_action.triggered.connect(self.pomodoro.resume)
            else:
                pomo_action = QAction("⏸️ 暂停番茄钟 / Pause", self)
                pomo_action.triggered.connect(self.pomodoro.pause)
            menu.addAction(pomo_action)

            stop_action = QAction("⏹️ 停止番茄钟 / Stop", self)
            stop_action.triggered.connect(self.pomodoro.stop)
            menu.addAction(stop_action)

            menu.addSeparator()

        # 缩放 / Scale
        scale_menu = menu.addMenu("🔍 缩放 / Scale")
        for s in [0.75, 1.0, 1.25, 1.5]:
            action = QAction(f"{int(s*100)}%", self)
            action.triggered.connect(lambda checked, sc=s: self._set_scale(sc))
            scale_menu.addAction(action)

        menu.addSeparator()

        # 退出 / Quit
        quit_action = QAction("❌ 退出 / Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_action)

        menu.exec_(self.mapToGlobal(pos))

    def _switch_pet(self, species: str):
        """切换宠物 / Switch pet"""
        old_pos_x = self.pet.x
        old_pos_y = self.pet.y
        self.pet = create_pet(species, self.cfg.pet_name)
        self.pet.x = old_pos_x
        self.pet.y = old_pos_y
        self.pet.on_speak = self._on_pet_speak
        self.config_mgr.update(pet_species=species)
        self.pet_changed.emit(species)
        self.pet.speak(f"你好！我是{PET_DISPLAY_NAMES[species].split()[1]}！")
        self.update()

    def _set_scale(self, scale: float):
        """设置缩放 / Set scale"""
        self.config_mgr.update(scale=scale)
        self.cfg.scale = scale
        self.update()

    def _on_pet_speak(self, text: str):
        """宠物说话回调 / Pet speak callback"""
        self._speech_text = text
        self._speech_timer.start(3000)
        self.update()

    def _clear_speech(self):
        """清除对话 / Clear speech"""
        self._speech_text = ""
        self.update()

    def _on_work_complete(self):
        """工作完成 / Work complete"""
        self.pet.speak(f"🎉 完成第{self.pomodoro.completed_cycles}个番茄！休息一下吧～")
        self.pet.change_state(PetState.HAPPY, 4)

    def _on_break_start(self):
        """休息开始 / Break start"""
        self.pet.speak("☕ 休息时间到！起来活动活动～")

    def _on_break_complete(self):
        """休息结束 / Break complete"""
        self.pet.speak("⏰ 休息结束，继续加油！")

    def _on_tick(self):
        """每帧更新 / Per-frame update"""
        import time
        now = time.time()
        if self._last_time == 0:
            dt = 0.016
        else:
            dt = now - self._last_time
        self._last_time = now

        # 更新宠物 / Update pet
        self.pet.update(dt, self.width(), self.height())

        # 更新番茄钟 / Update pomodoro
        if self.cfg.enable_pomodoro:
            self.pomodoro.update()

        self.update()

    # ===== 绘制 / Painting =====

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        scale = self.cfg.scale

        # 绘制系统监控信息条（如果启用）/ Draw system monitor bar if enabled
        if self.cfg.enable_system_monitor:
            self._draw_system_bar(painter)

        # 绘制番茄钟状态 / Draw pomodoro status
        if self.cfg.enable_pomodoro and self.pomodoro.state != PomodoroState.IDLE:
            self._draw_pomodoro_bar(painter)

        # 绘制宠物 / Draw pet
        self.pet.draw(painter, int(self.pet.x), int(self.pet.y), scale)

        # 绘制对话气泡 / Draw speech bubble
        if self._speech_text:
            self._draw_speech_bubble(painter)

        painter.end()

    def _draw_system_bar(self, painter: QPainter):
        """绘制系统监控信息条 / Draw system monitor bar"""
        cpu, mem = self.sys_monitor.get_status_tuple()
        text = f"💻 CPU {cpu:.0f}%  MEM {mem:.0f}%"

        font = QFont("Arial", 9)
        painter.setFont(font)
        metrics = painter.fontMetrics()
        tw = metrics.horizontalAdvance(text)
        th = metrics.height()

        padding = 6
        bar_w = tw + padding * 2
        bar_h = th + padding

        # 背景 / Background
        path = QPainterPath()
        path.addRoundedRect(QRectF(5, 5, bar_w, bar_h), 8, 8)
        painter.fillPath(path, QBrush(QColor(0, 0, 0, 140)))
        painter.setPen(QPen(QColor(255, 255, 255, 60), 1))
        painter.drawPath(path)

        # 文字 / Text
        painter.setPen(QColor(255, 255, 255, 220))
        painter.drawText(QRectF(5 + padding, 5 + padding // 2, tw, th), Qt.AlignLeft | Qt.AlignVCenter, text)

    def _draw_pomodoro_bar(self, painter: QPainter):
        """绘制番茄钟状态栏 / Draw pomodoro status bar"""
        state_text = "🍅 专注中" if self.pomodoro.state == PomodoroState.WORKING else "☕ 休息中"
        if self.pomodoro.state == PomodoroState.PAUSED:
            state_text = "⏸️ 已暂停"
        time_text = self.pomodoro.format_time()
        text = f"{state_text} {time_text}"

        font = QFont("Arial", 9, QFont.Bold)
        painter.setFont(font)
        metrics = painter.fontMetrics()
        tw = metrics.horizontalAdvance(text)
        th = metrics.height()

        padding = 6
        bar_w = tw + padding * 2
        bar_h = th + padding
        x = self.width() - bar_w - 5
        y = 5

        # 背景 / Background
        color = QColor(255, 100, 100, 160) if self.pomodoro.state == PomodoroState.WORKING else QColor(100, 200, 100, 160)
        path = QPainterPath()
        path.addRoundedRect(QRectF(x, y, bar_w, bar_h), 8, 8)
        painter.fillPath(path, QBrush(color))
        painter.setPen(QPen(QColor(255, 255, 255, 80), 1))
        painter.drawPath(path)

        # 进度条 / Progress bar
        progress = self.pomodoro.progress
        prog_h = 3
        painter.fillRect(QRectF(x + 4, y + bar_h - prog_h - 2, (bar_w - 8) * progress, prog_h),
                         QBrush(QColor(255, 255, 255, 180)))

        # 文字 / Text
        painter.setPen(QColor(255, 255, 255, 240))
        painter.drawText(QRectF(x + padding, y + padding // 2, tw, th), Qt.AlignLeft | Qt.AlignVCenter, text)

    def _draw_speech_bubble(self, painter: QPainter):
        """绘制对话气泡 / Draw speech bubble"""
        text = self._speech_text
        font = QFont("Arial", 10)
        painter.setFont(font)
        metrics = painter.fontMetrics()
        tw = metrics.horizontalAdvance(text)
        th = metrics.height()

        padding_x = 12
        padding_y = 8
        bubble_w = tw + padding_x * 2
        bubble_h = th + padding_y * 2

        # 气泡位置在宠物头顶 / Bubble above pet head
        bx = self.pet.x - bubble_w / 2
        by = self.pet.y - 80 * self.cfg.scale - bubble_h

        # 限制在窗口内 / Keep within window
        bx = max(5, min(self.width() - bubble_w - 5, bx))
        by = max(5, by)

        # 气泡背景 / Bubble background
        path = QPainterPath()
        path.addRoundedRect(QRectF(bx, by, bubble_w, bubble_h), 12, 12)
        # 小尾巴 / Tail
        tail_x = self.pet.x
        tail_x = max(bx + 15, min(bx + bubble_w - 15, tail_x))
        path.moveTo(tail_x - 6, by + bubble_h)
        path.lineTo(tail_x, by + bubble_h + 10)
        path.lineTo(tail_x + 6, by + bubble_h)
        path.closeSubpath()

        painter.fillPath(path, QBrush(QColor(255, 255, 255, 235)))
        painter.setPen(QPen(QColor(200, 200, 200, 180), 1.5))
        painter.drawPath(path)

        # 文字 / Text
        painter.setPen(QColor(50, 50, 50))
        painter.drawText(QRectF(bx + padding_x, by + padding_y // 2, tw, th),
                         Qt.AlignCenter, text)

    # ===== 鼠标事件 / Mouse events =====

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.globalPos() - self.frameGeometry().topLeft()
            # 点击宠物 = 抚摸 / Clicking pet = pet interaction
            self.pet.pet()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            event.accept()

    def mouseDoubleClickEvent(self, event):
        """双击 = 玩耍 / Double click = play"""
        if event.button() == Qt.LeftButton:
            self.pet.play()
            event.accept()
