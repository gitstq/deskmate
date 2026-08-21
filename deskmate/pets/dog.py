"""
狗狗角色 / Dog character
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QRectF
import math

from ..pet import BasePet, PetState


class DogPet(BasePet):
    """小狗狗 / Little Dog"""
    SPECIES_NAME = "dog"
    DISPLAY_NAME = "小狗狗"

    def __init__(self, name="旺财"):
        super().__init__(name)
        self.body_color = QColor("#D4A574")
        self.belly_color = QColor("#F5DEB3")
        self.ear_color = QColor("#8B6914")

    def draw(self, painter: QPainter, x: int, y: int, scale: float = 1.0):
        painter.save()
        painter.translate(x, y)
        painter.scale(scale * self.direction, scale)
        painter.setRenderHint(QPainter.Antialiasing)

        frame = self.anim_frame
        state = self.state
        breathe = math.sin(frame * math.pi / 2) * 2

        body_w, body_h = 55, 40
        body_y = 12 + breathe

        # 阴影 / Shadow
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 2, body_y + body_h - 2, body_w, 8))

        # 尾巴（摇尾巴）/ Tail (wagging)
        tail_wag = math.sin(frame * math.pi) * 25 if state in (PetState.HAPPY, PetState.PLAYING) else math.sin(frame * math.pi / 2) * 10
        painter.save()
        painter.translate(-body_w/2 + 2, body_y + 10)
        painter.rotate(-30 + tail_wag)
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#B8956A"), 1.5))
        painter.drawRoundedRect(QRectF(-4, -18, 8, 20), 4, 4)
        painter.restore()

        # 身体 / Body
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#B8956A"), 1.5))
        painter.drawEllipse(QRectF(-body_w/2, body_y, body_w, body_h))

        # 肚皮 / Belly
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 12, body_y + 14, body_w - 24, body_h - 20))

        # 腿 / Legs
        leg_off = math.sin(frame * math.pi) * 4 if state == PetState.WALKING else 0
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#B8956A"), 1))
        painter.drawRoundedRect(QRectF(-20, body_y + body_h - 4 + leg_off, 11, 14), 3, 3)
        painter.drawRoundedRect(QRectF(9, body_y + body_h - 4 - leg_off, 11, 14), 3, 3)

        # 头部 / Head
        head_r = 25
        head_y = body_y - 16

        # 垂耳 / Floppy ears
        ear_swing = math.sin(frame * math.pi / 2) * 5 if state == PetState.WALKING else 0
        painter.setBrush(QBrush(self.ear_color))
        painter.setPen(QPen(QColor("#6B5010"), 1))
        # 左耳 / Left ear
        painter.save()
        painter.translate(-18, head_y - 5)
        painter.rotate(-10 + ear_swing)
        painter.drawRoundedRect(QRectF(-7, 0, 14, 24), 5, 5)
        painter.restore()
        # 右耳 / Right ear
        painter.save()
        painter.translate(18, head_y - 5)
        painter.rotate(10 - ear_swing)
        painter.drawRoundedRect(QRectF(-7, 0, 14, 24), 5, 5)
        painter.restore()

        # 脸 / Face
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#B8956A"), 1.5))
        painter.drawEllipse(QRectF(-head_r, head_y - head_r, head_r * 2, head_r * 2))

        # 口鼻区域 / Muzzle
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-12, head_y + 2, 24, 16))

        # 眼睛 / Eyes
        eye_y = head_y - 4
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-13, eye_y - 3, 9, 7), 0, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 3, 9, 7), 0, 180 * 16)
        elif state in (PetState.HAPPY, PetState.PLAYING):
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-13, eye_y - 1, 9, 7), 180 * 16, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 1, 9, 7), 180 * 16, 180 * 16)
        else:
            painter.setBrush(QBrush(QColor("#2C3E50")))
            painter.setPen(Qt.NoPen)
            blink = (frame == 0)
            if blink:
                painter.setPen(QPen(QColor("#333"), 1.5))
                painter.drawLine(-13, eye_y, -4, eye_y)
                painter.drawLine(4, eye_y, 13, eye_y)
            else:
                er = 4.5 if state == PetState.CURIOUS else 3.5
                painter.drawEllipse(QRectF(-11 - er/2, eye_y - er, er, er * 2))
                painter.drawEllipse(QRectF(5 - er/2, eye_y - er, er, er * 2))
                painter.setBrush(QBrush(QColor("white")))
                painter.drawEllipse(QRectF(-10, eye_y - 2.5, 1.5, 1.5))
                painter.drawEllipse(QRectF(6, eye_y - 2.5, 1.5, 1.5))

        # 鼻子 / Nose
        painter.setBrush(QBrush(QColor("#2C3E50")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-4, head_y + 4, 8, 6))

        # 嘴巴 / Mouth
        painter.setPen(QPen(QColor("#333"), 1.5))
        if state == PetState.EATING:
            painter.drawArc(QRectF(-5, head_y + 9, 10, 7), 0, 180 * 16)
        elif state in (PetState.HAPPY, PetState.PLAYING):
            painter.drawArc(QRectF(-7, head_y + 8, 14, 9), 0, 180 * 16)
            # 舌头 / Tongue
            painter.setBrush(QBrush(QColor("#FF6B9D")))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF(-3, head_y + 13, 6, 6), 2, 2)
        elif state == PetState.SAD:
            painter.drawArc(QRectF(-5, head_y + 13, 10, 5), 180 * 16, 180 * 16)
        else:
            painter.drawLine(0, head_y + 10, -4, head_y + 13)
            painter.drawLine(0, head_y + 10, 4, head_y + 13)

        # 睡觉Z / Sleep Z
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#74B9FF"), 2))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            z_off = frame * 3
            painter.drawText(22, head_y - 20 - z_off, "z")
            painter.drawText(30, head_y - 30 - z_off, "Z")

        # 开心特效 / Happy sparkles
        if state in (PetState.HAPPY, PetState.PLAYING):
            painter.setPen(QPen(QColor("#FFD93D"), 2))
            for angle in [0, 72, 144, 216, 288]:
                rad = math.radians(angle + frame * 36)
                sx = math.cos(rad) * 38
                sy = head_y + math.sin(rad) * 32 - 8
                painter.drawText(int(sx) - 3, int(sy), "★")

        painter.restore()

    def get_bounding_size(self, scale: float = 1.0):
        return (int(95 * scale), int(95 * scale))
