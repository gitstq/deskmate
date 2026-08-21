"""
宠物基类 - 定义所有桌面伴侣的通用行为与状态机
Pet base class - defines common behavior and state machine for all companions
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Optional
import random
import time


class PetState(Enum):
    """宠物状态枚举 / Pet states"""
    IDLE = "idle"             # 待机 / Idle
    WALKING = "walking"       # 行走 / Walking
    SLEEPING = "sleeping"     # 睡眠 / Sleeping
    EATING = "eating"         # 进食 / Eating
    PLAYING = "playing"       # 玩耍 / Playing
    HAPPY = "happy"           # 开心 / Happy
    SAD = "sad"               # 难过 / Sad
    CURIOUS = "curious"       # 好奇 / Curious


class Mood(Enum):
    """心情等级 / Mood levels"""
    VERY_HAPPY = 5
    HAPPY = 4
    NORMAL = 3
    UNHAPPY = 2
    SAD = 1


@dataclass
class PetStats:
    """宠物属性数值 / Pet stats"""
    hunger: int = 80          # 饱食度 0-100 / Fullness
    happiness: int = 70       # 快乐度 0-100 / Happiness
    energy: int = 90          # 精力值 0-100 / Energy
    cleanliness: int = 85     # 清洁度 0-100 / Cleanliness

    def clamp(self):
        """限制数值范围 / Clamp values to 0-100"""
        for attr in ['hunger', 'happiness', 'energy', 'cleanliness']:
            val = getattr(self, attr)
            setattr(self, attr, max(0, min(100, val)))

    @property
    def overall_mood(self) -> Mood:
        """综合心情 / Overall mood"""
        avg = (self.hunger + self.happiness + self.energy + self.cleanliness) / 4
        if avg >= 85:
            return Mood.VERY_HAPPY
        elif avg >= 70:
            return Mood.HAPPY
        elif avg >= 50:
            return Mood.NORMAL
        elif avg >= 30:
            return Mood.UNHAPPY
        return Mood.SAD


class BasePet:
    """
    宠物基类 / Base pet class
    所有具体宠物角色继承此类，实现各自的绘制方法
    """

    # 子类覆盖 / Subclasses override
    SPECIES_NAME = "base"
    DISPLAY_NAME = "Base Pet"
    DEFAULT_COLOR = "#888888"

    def __init__(self, name: str = "Mate"):
        self.name = name
        self.stats = PetStats()
        self.state = PetState.IDLE
        self.state_start_time = time.time()
        self.state_duration = 5.0  # 默认状态持续秒数

        # 位置与移动 / Position and movement
        self.x = 200.0
        self.y = 200.0
        self.target_x = None
        self.target_y = None
        self.speed = 2.0
        self.direction = 1  # 1=右, -1=左 / 1=right, -1=left

        # 动画帧 / Animation frame
        self.anim_frame = 0
        self.anim_timer = 0.0
        self.frame_interval = 0.15

        # 回调 / Callbacks
        self.on_state_change: Optional[Callable[[PetState, PetState], None]] = None
        self.on_speak: Optional[Callable[[str], None]] = None

        # 对话气泡 / Speech bubbles
        self.speech_text = ""
        self.speech_until = 0

        # 上次属性衰减时间 / Last stat decay time
        self.last_decay = time.time()

    def update(self, dt: float, screen_width: int, screen_height: int):
        """
        每帧更新 / Per-frame update
        :param dt: 距上帧的秒数 / Seconds since last frame
        :param screen_width: 屏幕宽度 / Screen width
        :param screen_height: 屏幕高度 / Screen height
        """
        now = time.time()

        # 属性衰减 / Stat decay (every 30s real time, small decrement)
        if now - self.last_decay >= 30:
            self.stats.hunger -= random.randint(1, 3)
            self.stats.happiness -= random.randint(0, 2)
            self.stats.energy -= random.randint(0, 2)
            self.stats.cleanliness -= random.randint(0, 1)
            self.stats.clamp()
            self.last_decay = now
            self._check_needs()

        # 状态超时自动切换 / Auto state transition on timeout
        if now - self.state_start_time >= self.state_duration:
            self._auto_transition(screen_width, screen_height)

        # 移动逻辑 / Movement logic
        if self.state == PetState.WALKING and self.target_x is not None:
            dx = self.target_x - self.x
            if abs(dx) < self.speed:
                self.x = self.target_x
                self.target_x = None
                self.change_state(PetState.IDLE, random.uniform(2, 5))
            else:
                self.x += self.speed if dx > 0 else -self.speed
                self.direction = 1 if dx > 0 else -1

        # 边界限制 / Boundary
        self.x = max(30, min(screen_width - 30, self.x))
        self.y = max(30, min(screen_height - 30, self.y))

        # 动画帧推进 / Advance animation frame
        self.anim_timer += dt
        if self.anim_timer >= self.frame_interval:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4

        # 清除过期对话 / Clear expired speech
        if self.speech_text and now > self.speech_until:
            self.speech_text = ""

    def _auto_transition(self, screen_width: int, screen_height: int):
        """状态自动切换 / Automatic state transition"""
        mood = self.stats.overall_mood
        r = random.random()

        if self.stats.energy < 20:
            self.change_state(PetState.SLEEPING, random.uniform(8, 15))
            return

        if self.stats.hunger < 25:
            self.speak("🍖 好饿啊...")
            self.change_state(PetState.SAD, random.uniform(2, 4))
            return

        if mood in (Mood.VERY_HAPPY, Mood.HAPPY) and r < 0.3:
            self.change_state(PetState.PLAYING, random.uniform(3, 6))
            return

        if r < 0.4:
            # 随机行走 / Random walk
            self.target_x = random.uniform(50, screen_width - 50)
            self.change_state(PetState.WALKING, random.uniform(3, 8))
        elif r < 0.6:
            self.change_state(PetState.CURIOUS, random.uniform(2, 4))
        elif r < 0.75 and self.stats.energy < 50:
            self.change_state(PetState.SLEEPING, random.uniform(5, 10))
        else:
            self.change_state(PetState.IDLE, random.uniform(2, 5))

    def _check_needs(self):
        """检查需求并提示 / Check needs and notify"""
        if self.stats.hunger < 30:
            self.speak("肚子咕咕叫了～")
        elif self.stats.happiness < 30:
            self.speak("有点无聊，陪我玩嘛～")
        elif self.stats.energy < 25:
            self.speak("好困啊...")

    def change_state(self, new_state: PetState, duration: float = 5.0):
        """切换状态 / Change state"""
        old = self.state
        self.state = new_state
        self.state_start_time = time.time()
        self.state_duration = duration
        if self.on_state_change and old != new_state:
            self.on_state_change(old, new_state)

    def speak(self, text: str, duration: float = 3.0):
        """显示对话气泡 / Show speech bubble"""
        self.speech_text = text
        self.speech_until = time.time() + duration
        if self.on_speak:
            self.on_speak(text)

    # ===== 交互动作 / Interaction actions =====

    def feed(self):
        """喂食 / Feed"""
        self.stats.hunger = min(100, self.stats.hunger + 30)
        self.stats.happiness = min(100, self.stats.happiness + 5)
        self.change_state(PetState.EATING, 3.0)
        self.speak("😋 好好吃！")

    def play(self):
        """玩耍 / Play"""
        self.stats.happiness = min(100, self.stats.happiness + 25)
        self.stats.energy = max(0, self.stats.energy - 10)
        self.change_state(PetState.PLAYING, 4.0)
        self.speak("🎉 好开心！")

    def pet(self):
        """抚摸 / Pet"""
        self.stats.happiness = min(100, self.stats.happiness + 10)
        self.change_state(PetState.HAPPY, 2.5)
        self.speak("😊 嘿嘿～")

    def sleep(self):
        """睡觉 / Sleep"""
        self.stats.energy = min(100, self.stats.energy + 40)
        self.change_state(PetState.SLEEPING, 6.0)
        self.speak("💤 晚安～")

    def clean(self):
        """清洁 / Clean"""
        self.stats.cleanliness = 100
        self.stats.happiness = min(100, self.stats.happiness + 5)
        self.change_state(PetState.HAPPY, 2.0)
        self.speak("✨ 干干净净！")

    # ===== 绘制方法（子类实现） / Draw method (subclass implements) =====

    def draw(self, painter, x: int, y: int, scale: float = 1.0):
        """
        使用QPainter绘制宠物 / Draw pet using QPainter
        子类必须重写 / Subclasses must override
        """
        raise NotImplementedError

    def get_bounding_size(self, scale: float = 1.0) -> tuple:
        """获取宠物占据的宽高 / Get pet bounding width and height"""
        return (int(80 * scale), int(80 * scale))
