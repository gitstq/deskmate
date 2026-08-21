"""
宠物角色定义 / Pet species definitions
每个角色使用QPainter程序化绘制，无需外部图片素材
Each character is drawn programmatically with QPainter, no external image assets needed
"""

from .cat import CatPet
from .dog import DogPet
from .bunny import BunnyPet
from .fox import FoxPet

# 宠物注册表 / Pet registry
PET_REGISTRY = {
    "cat": CatPet,
    "dog": DogPet,
    "bunny": BunnyPet,
    "fox": FoxPet,
}

PET_DISPLAY_NAMES = {
    "cat": "🐱 小猫咪",
    "dog": "🐶 小狗狗",
    "bunny": "🐰 小兔子",
    "fox": "🦊 小狐狸",
}


def create_pet(species: str, name: str = "Mate"):
    """工厂方法创建宠物 / Factory method to create a pet"""
    cls = PET_REGISTRY.get(species.lower())
    if cls is None:
        raise ValueError(f"Unknown pet species: {species}. Available: {list(PET_REGISTRY.keys())}")
    return cls(name)
