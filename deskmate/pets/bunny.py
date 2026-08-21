"""
兔子角色 / Bunny character
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QRectF
import math

from ..pet import BasePet, PetState


class BunnyPet(BasePet):
    """小兔子 / Little Bunny"""
    SPECIES_NAME = "bunny"
    DISPLAY_NAME = "小兔子"

    def __init__(self, name="雪球"):
        super().__init__(name)
        self.body_color = QColor("#F8F8FF")
        self.belly_color = QColor("#FFE4E1")
        self.ear_color = QColor("#FFB6C1")

    def draw(self, painter: QPainter, x: int, y: int, scale: float = 1.0):
        painter.save()
        painter.translate(x, y)
        painter.scale(scale * self.direction, scale)
        painter.setRenderHint(QPainter.Antialiasing)

        frame = self.anim_frame
        state = self.state
        breathe = math.sin(frame * math.pi / 2) * 2

        body_w, body_h = 45, 42
        body_y = 15 + breathe

        # 阴影 / Shadow
        painter.setBrush(QBrush(QColor(0, 0, 0, 35)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 2, body_y + body_h, body_w, 7))

        # 身体 / Body (rounder for bunny)
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#DDD"), 1.5))
        painter.drawEllipse(QRectF(-body_w/2, body_y, body_w, body_h))

        # 肚皮 / Belly
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 8, body_y + 14, body_w - 16, body_h - 20))

        # 短尾巴 / Cotton tail
        painter.setBrush(QBrush(QColor("white")))
        painter.setPen(QPen(QColor("#EEE"), 1))
        painter.drawEllipse(QRectF(-body_w/2 - 6, body_y + 15, 12, 12))

        # 腿 / Legs (hop animation)
        hop = abs(math.sin(frame * math.pi / 2)) * 6 if state == PetState.WALKING else 0
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#DDD"), 1))
        painter.drawEllipse(QRectF(-16, body_y + body_h - 4 - hop, 12, 12))
        painter.drawEllipse(QRectF(4, body_y + body_h - 4 - hop, 12, 12))

        # 头部 / Head
        head_r = 23
        head_y = body_y - 14

        # 长耳朵 / Long ears
        ear_wiggle = math.sin(frame * math.pi / 2) * 8 if state in (PetState.CURIOUS, PetState.HAPPY) else math.sin(frame * math.pi / 2) * 3
        # 左耳 / Left ear
        painter.save()
        painter.translate(-10, head_y - head_r + 2)
        painter.rotate(-8 + ear_wiggle)
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#DDD"), 1.5))
        painter.drawRoundedRect(QRectF(-5, -30, 10, 34), 5, 5)
        # 耳内 / Inner ear
        painter.setBrush(QBrush(self.ear_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(-3, -26, 6, 26), 3, 3)
        painter.restore()
        # 右耳 / Right ear
        painter.save()
        painter.translate(10, head_y - head_r + 2)
        painter.rotate(8 - ear_wiggle)
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#DDD"), 1.5))
        painter.drawRoundedRect(QRectF(-5, -30, 10, 34), 5, 5)
        painter.setBrush(QBrush(self.ear_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(-3, -26, 6, 26), 3, 3)
        painter.restore()

        # 脸 / Face
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#DDD"), 1.5))
        painter.drawEllipse(QRectF(-head_r, head_y - head_r, head_r * 2, head_r * 2))

        # 眼睛 / Eyes
        eye_y = head_y - 2
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-12, eye_y - 3, 8, 7), 0, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 3, 8, 7), 0, 180 * 16)
        elif state in (PetState.HAPPY, PetState.PLAYING):
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-12, eye_y - 1, 8, 7), 180 * 16, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 1, 8, 7), 180 * 16, 180 * 16)
        else:
            painter.setBrush(QBrush(QColor("#FF6B9D")))
            painter.setPen(Qt.NoPen)
            blink = (frame == 0)
            if blink:
                painter.setPen(QPen(QColor("#333"), 1.5))
                painter.drawLine(-12, eye_y, -4, eye_y)
                painter.drawLine(4, eye_y, 12, eye_y)
            else:
                er = 4 if state == PetState.CURIOUS else 3
                painter.drawEllipse(QRectF(-10 - er/2, eye_y - er, er, er * 2))
                painter.drawEllipse(QRectF(6 - er/2, eye_y - er, er, er * 2))
                painter.setBrush(QBrush(QColor("white")))
                painter.drawEllipse(QRectF(-9, eye_y - 2, 1.5, 1.5))
                painter.drawEllipse(QRectF(7, eye_y - 2, 1.5, 1.5))

        # 鼻子 / Nose (pink bunny nose)
        painter.setBrush(QBrush(QColor("#FF6B9D")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-3, head_y + 5, 6, 4))

        # 嘴巴 / Mouth
        painter.setPen(QPen(QColor("#333"), 1.5))
        if state == PetState.EATING:
            painter.drawArc(QRectF(-4, head_y + 8, 8, 6), 0, 180 * 16)
        elif state in (PetState.HAPPY, PetState.PLAYING):
            painter.drawArc(QRectF(-5, head_y + 7, 10, 7), 0, 180 * 16)
        elif state == PetState.SAD:
            painter.drawArc(QRectF(-4, head_y + 11, 8, 5), 180 * 16, 180 * 16)
        else:
            # Y形嘴 / Y-shaped mouth
            painter.drawLine(0, head_y + 9, 0, head_y + 12)
            painter.drawLine(0, head_y + 12, -3, head_y + 14)
            painter.drawLine(0, head_y + 12, 3, head_y + 14)

        # 腮红 / Blush
        painter.setBrush(QBrush(QColor(255, 182, 193, 120)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-16, head_y + 3, 7, 5))
        painter.drawEllipse(QRectF(9, head_y + 3, 7, 5))

        # 睡觉Z / Sleep Z
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#74B9FF"), 2))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            z_off = frame * 3
            painter.drawText(18, head_y - 25 - z_off, "z")
            painter.drawText(25, head_y - 33 - z_off, "Z")

        # 开心特效 / Happy effect
        if state in (PetState.HAPPY, PetState.PLAYING):
            painter.setPen(QPen(QColor("#FFB6C1"), 2))
            for angle in [45, 135, 225, 315]:
                rad = math.radians(angle + frame * 45)
                sx = math.cos(rad) * 34
                sy = head_y + math.sin(rad) * 28 - 5
                painter.drawText(int(sx) - 2, int(sy), "♡")

        painter.restore()

    def get_bounding_size(self, scale: float = 1.0):
        return (int(85 * scale), int(110 * scale))
