"""
配置管理 / Configuration management
使用JSON文件持久化用户配置 / Persist user config using JSON file
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".deskmate")
DEFAULT_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_DIR, "config.json")


@dataclass
class DeskMateConfig:
    """DeskMate 配置 / DeskMate configuration"""
    pet_species: str = "cat"           # 宠物种类 / Pet species
    pet_name: str = "Mate"             # 宠物名字 / Pet name
    scale: float = 1.0                 # 显示缩放 / Display scale
    always_on_top: bool = True         # 始终置顶 / Always on top
    transparency: int = 0               # 背景透明度(0=完全透明) / Background transparency
    start_on_boot: bool = False         # 开机启动 / Start on boot
    enable_pomodoro: bool = True        # 启用番茄钟 / Enable pomodoro
    pomodoro_work_minutes: int = 25     # 番茄钟工作时长 / Pomodoro work minutes
    pomodoro_break_minutes: int = 5     # 番茄钟休息时长 / Pomodoro break minutes
    enable_system_monitor: bool = True  # 启用系统监控 / Enable system monitor
    sound_enabled: bool = False          # 音效开关 / Sound enabled
    language: str = "zh_CN"             # 界面语言 / UI language

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DeskMateConfig":
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


class ConfigManager:
    """配置管理器 / Configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = DeskMateConfig()
        self.load()

    def load(self):
        """从文件加载配置 / Load config from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.config = DeskMateConfig.from_dict(data)
        except (json.JSONDecodeError, IOError, TypeError):
            # 配置损坏时使用默认值 / Use defaults if config is corrupted
            self.config = DeskMateConfig()

    def save(self):
        """保存配置到文件 / Save config to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def update(self, **kwargs):
        """更新配置字段 / Update config fields"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self.save()

    def get(self, key: str, default=None):
        """获取配置值 / Get config value"""
        return getattr(self.config, key, default)
