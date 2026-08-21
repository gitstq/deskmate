"""
番茄钟计时器 / Pomodoro timer
帮助用户专注工作，定时提醒休息 / Help users focus and remind them to take breaks
"""

from enum import Enum
from typing import Callable, Optional
import time


class PomodoroState(Enum):
    """番茄钟状态 / Pomodoro states"""
    IDLE = "idle"           # 未开始 / Not started
    WORKING = "working"     # 工作中 / Working
    ON_BREAK = "on_break"   # 休息中 / On break
    PAUSED = "paused"       # 已暂停 / Paused


class PomodoroTimer:
    """
    番茄钟计时器 / Pomodoro timer
    支持工作/休息循环，完成时触发回调 / Supports work/break cycles, triggers callbacks on completion
    """

    def __init__(self, work_minutes: int = 25, break_minutes: int = 5):
        self.work_seconds = work_minutes * 60
        self.break_seconds = break_minutes * 60
        self.state = PomodoroState.IDLE
        self.remaining = self.work_seconds
        self._last_tick = None
        self.completed_cycles = 0

        # 回调 / Callbacks
        self.on_work_start: Optional[Callable] = None
        self.on_break_start: Optional[Callable] = None
        self.on_work_complete: Optional[Callable] = None
        self.on_break_complete: Optional[Callable] = None
        self.on_tick: Optional[Callable[[int], None]] = None  # remaining seconds

    def start(self):
        """开始番茄钟 / Start pomodoro"""
        if self.state in (PomodoroState.IDLE, PomodoroState.PAUSED):
            self.state = PomodoroState.WORKING
            self.remaining = self.work_seconds
            self._last_tick = time.time()
            if self.on_work_start:
                self.on_work_start()

    def pause(self):
        """暂停 / Pause"""
        if self.state in (PomodoroState.WORKING, PomodoroState.ON_BREAK):
            self.state = PomodoroState.PAUSED

    def resume(self):
        """继续 / Resume"""
        if self.state == PomodoroState.PAUSED:
            self._last_tick = time.time()
            # 恢复到之前的状态 / Restore previous state
            if self.remaining <= self.break_seconds and self.completed_cycles > 0:
                self.state = PomodoroState.ON_BREAK
            else:
                self.state = PomodoroState.WORKING

    def stop(self):
        """停止 / Stop"""
        self.state = PomodoroState.IDLE
        self.remaining = self.work_seconds
        self.completed_cycles = 0

    def skip_break(self):
        """跳过休息 / Skip break"""
        if self.state == PomodoroState.ON_BREAK:
            self._start_work()

    def _start_work(self):
        self.state = PomodoroState.WORKING
        self.remaining = self.work_seconds
        self._last_tick = time.time()
        if self.on_work_start:
            self.on_work_start()

    def _start_break(self):
        self.state = PomodoroState.ON_BREAK
        self.remaining = self.break_seconds
        self._last_tick = time.time()
        if self.on_break_start:
            self.on_break_start()

    def update(self) -> bool:
        """
        每帧调用，更新倒计时 / Call per frame to update countdown
        Returns True if state changed / 状态变化时返回True
        """
        if self.state not in (PomodoroState.WORKING, PomodoroState.ON_BREAK):
            return False

        now = time.time()
        if self._last_tick is None:
            self._last_tick = now
            return False

        elapsed = now - self._last_tick
        self._last_tick = now
        self.remaining = max(0, self.remaining - elapsed)

        if self.on_tick:
            self.on_tick(int(self.remaining))

        if self.remaining <= 0:
            if self.state == PomodoroState.WORKING:
                self.completed_cycles += 1
                if self.on_work_complete:
                    self.on_work_complete()
                self._start_break()
            else:
                if self.on_break_complete:
                    self.on_break_complete()
                self._start_work()
            return True

        return False

    @property
    def progress(self) -> float:
        """当前阶段进度 0-1 / Current phase progress 0-1"""
        total = self.break_seconds if self.state == PomodoroState.ON_BREAK else self.work_seconds
        if total == 0:
            return 0
        return 1.0 - (self.remaining / total)

    def format_time(self) -> str:
        """格式化剩余时间 MM:SS / Format remaining time as MM:SS"""
        mins = int(self.remaining) // 60
        secs = int(self.remaining) % 60
        return f"{mins:02d}:{secs:02d}"
