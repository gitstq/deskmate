"""
狐狸角色 / Fox character
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QRectF
import math

from ..pet import BasePet, PetState


class FoxPet(BasePet):
    """小狐狸 / Little Fox"""
    SPECIES_NAME = "fox"
    DISPLAY_NAME = "小狐狸"

    def __init__(self, name="小火"):
        super().__init__(name)
        self.body_color = QColor("#FF6B35")
        self.belly_color = QColor("#FFF8F0")
        self.ear_color = QColor("#CC4400")
        self.tail_tip = QColor("white")

    def draw(self, painter: QPainter, x: int, y: int, scale: float = 1.0):
        painter.save()
        painter.translate(x, y)
        painter.scale(scale * self.direction, scale)
        painter.setRenderHint(QPainter.Antialiasing)

        frame = self.anim_frame
        state = self.state
        breathe = math.sin(frame * math.pi / 2) * 2

        body_w, body_h = 52, 40
        body_y = 12 + breathe

        # 阴影 / Shadow
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 2, body_y + body_h - 2, body_w, 8))

        # 大尾巴 / Big bushy tail
        tail_wag = math.sin(frame * math.pi) * 20 if state in (PetState.HAPPY, PetState.PLAYING) else math.sin(frame * math.pi / 2) * 8
        painter.save()
        painter.translate(-body_w/2 + 5, body_y + 8)
        painter.rotate(-20 + tail_wag)
        # 尾巴主体 / Tail body
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#CC4400"), 1.5))
        painter.drawRoundedRect(QRectF(-6, -25, 12, 30), 6, 6)
        # 尾巴尖 / Tail tip
        painter.setBrush(QBrush(self.tail_tip))
        painter.setPen(QPen(QColor("#EEE"), 1))
        painter.drawRoundedRect(QRectF(-6, -25, 12, 12), 6, 6)
        painter.restore()

        # 身体 / Body
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#CC4400"), 1.5))
        painter.drawEllipse(QRectF(-body_w/2, body_y, body_w, body_h))

        # 肚皮 / Belly (white chest)
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 10, body_y + 12, body_w - 20, body_h - 16))

        # 腿 / Legs
        leg_off = math.sin(frame * math.pi) * 4 if state == PetState.WALKING else 0
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#CC4400"), 1))
        painter.drawRoundedRect(QRectF(-18, body_y + body_h - 4 + leg_off, 10, 13), 3, 3)
        painter.drawRoundedRect(QRectF(8, body_y + body_h - 4 - leg_off, 10, 13), 3, 3)
        # 白爪 / White paws
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(-18, body_y + body_h + 4 + leg_off, 10, 5), 2, 2)
        painter.drawRoundedRect(QRectF(8, body_y + body_h + 4 - leg_off, 10, 5), 2, 2)

        # 头部 / Head
        head_r = 25
        head_y = body_y - 16

        # 尖耳朵 / Pointy ears
        ear_tilt = 15 if state == PetState.SAD else 0
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#CC4400"), 1.5))
        # 左耳 / Left ear
        painter.save()
        painter.translate(-15, head_y - 10)
        painter.rotate(-30 + ear_tilt)
        painter.drawPolygon(*[Qt.QPoint(-7, 5), Qt.QPoint(0, -22), Qt.QPoint(7, 5)])
        painter.restore()
        # 右耳 / Right ear
        painter.save()
        painter.translate(15, head_y - 10)
        painter.rotate(30 - ear_tilt)
        painter.drawPolygon(*[Qt.QPoint(-7, 5), Qt.QPoint(0, -22), Qt.QPoint(7, 5)])
        painter.restore()
        # 耳内 / Inner ear
        painter.setBrush(QBrush(self.ear_color))
        painter.setPen(Qt.NoPen)
        painter.save()
        painter.translate(-15, head_y - 10)
        painter.rotate(-30 + ear_tilt)
        painter.drawPolygon(*[Qt.QPoint(-3, 2), Qt.QPoint(0, -14), Qt.QPoint(3, 2)])
        painter.restore()
        painter.save()
        painter.translate(15, head_y - 10)
        painter.rotate(30 - ear_tilt)
        painter.drawPolygon(*[Qt.QPoint(-3, 2), Qt.QPoint(0, -14), Qt.QPoint(3, 2)])
        painter.restore()

        # 脸 / Face
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#CC4400"), 1.5))
        painter.drawEllipse(QRectF(-head_r, head_y - head_r, head_r * 2, head_r * 2))

        # 白色面部区域 / White face mask
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-14, head_y - 2, 28, 18))

        # 眼睛 / Eyes (amber color for fox)
        eye_y = head_y - 5
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-13, eye_y - 3, 9, 7), 0, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 3, 9, 7), 0, 180 * 16)
        elif state in (PetState.HAPPY, PetState.PLAYING):
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-13, eye_y - 1, 9, 7), 180 * 16, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 1, 9, 7), 180 * 16, 180 * 16)
        else:
            painter.setBrush(QBrush(QColor("#DAA520")))
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
                # 竖瞳 / Vertical slit pupil
                painter.setBrush(QBrush(QColor("#2C3E50")))
                painter.drawEllipse(QRectF(-10.5, eye_y - er + 0.5, 1.5, er * 2 - 1))
                painter.drawEllipse(QRectF(5.5, eye_y - er + 0.5, 1.5, er * 2 - 1))
                # 高光 / Highlight
                painter.setBrush(QBrush(QColor("white")))
                painter.drawEllipse(QRectF(-10, eye_y - 2.5, 1.5, 1.5))
                painter.drawEllipse(QRectF(6, eye_y - 2.5, 1.5, 1.5))

        # 鼻子 / Nose (black triangle)
        painter.setBrush(QBrush(QColor("#2C3E50")))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(*[Qt.QPoint(-4, head_y + 6), Qt.QPoint(4, head_y + 6), Qt.QPoint(0, head_y + 11)])

        # 嘴巴 / Mouth
        painter.setPen(QPen(QColor("#333"), 1.5))
        if state == PetState.EATING:
            painter.drawArc(QRectF(-5, head_y + 10, 10, 7), 0, 180 * 16)
        elif state in (PetState.HAPPY, PetState.PLAYING):
            painter.drawArc(QRectF(-6, head_y + 9, 12, 8), 0, 180 * 16)
        elif state == PetState.SAD:
            painter.drawArc(QRectF(-5, head_y + 14, 10, 5), 180 * 16, 180 * 16)
        else:
            painter.drawLine(0, head_y + 11, -4, head_y + 14)
            painter.drawLine(0, head_y + 11, 4, head_y + 14)

        # 睡觉Z / Sleep Z
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#74B9FF"), 2))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            z_off = frame * 3
            painter.drawText(20, head_y - 22 - z_off, "z")
            painter.drawText(28, head_y - 32 - z_off, "Z")

        # 开心特效 / Happy sparkles (fire themed)
        if state in (PetState.HAPPY, PetState.PLAYING):
            painter.setPen(QPen(QColor("#FF6B35"), 2))
            for angle in [0, 60, 120, 180, 240, 300]:
                rad = math.radians(angle + frame * 30)
                sx = math.cos(rad) * 36
                sy = head_y + math.sin(rad) * 30 - 8
                painter.drawText(int(sx) - 3, int(sy), "🔥")

        painter.restore()

    def get_bounding_size(self, scale: float = 1.0):
        return (int(100 * scale), int(95 * scale))
