"""
猫咪角色 / Cat character
"""

from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QRectF
import math

from ..pet import BasePet, PetState


class CatPet(BasePet):
    """小猫咪 / Little Cat"""
    SPECIES_NAME = "cat"
    DISPLAY_NAME = "小猫咪"
    DEFAULT_COLOR = "#FF9F43"

    def __init__(self, name="咪咪"):
        super().__init__(name)
        self.body_color = QColor("#FF9F43")
        self.belly_color = QColor("#FFE0B2")
        self.ear_color = QColor("#FFAB91")

    def draw(self, painter: QPainter, x: int, y: int, scale: float = 1.0):
        painter.save()
        painter.translate(x, y)
        painter.scale(scale * self.direction, scale)
        painter.setRenderHint(QPainter.Antialiasing)

        frame = self.anim_frame
        state = self.state

        # 呼吸/待机动画偏移 / Breathing/idle animation offset
        breathe = math.sin(frame * math.pi / 2) * 2

        # ===== 身体 / Body =====
        body_w, body_h = 50, 42
        body_y = 10 + breathe

        # 阴影 / Shadow
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 2, body_y + body_h - 2, body_w, 8))

        # 尾巴 / Tail
        tail_wag = math.sin(frame * math.pi / 2) * 15
        if state == PetState.HAPPY or state == PetState.PLAYING:
            tail_wag = math.sin(frame * math.pi) * 30
        painter.setBrush(QBrush(self.body_color))
        painter.drawRoundedRect(QRectF(body_w/2 - 5, body_y + 5, 22, 8), 4, 4)
        # 尾巴尖 / Tail tip
        painter.save()
        painter.translate(body_w/2 + 15, body_y + 9)
        painter.rotate(tail_wag)
        painter.drawRoundedRect(QRectF(0, -4, 14, 8), 4, 4)
        painter.restore()

        # 身体椭圆 / Body ellipse
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#E08A3C"), 1.5))
        painter.drawEllipse(QRectF(-body_w/2, body_y, body_w, body_h))

        # 肚皮 / Belly
        painter.setBrush(QBrush(self.belly_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-body_w/2 + 10, body_y + 12, body_w - 20, body_h - 18))

        # 腿 / Legs (animated when walking)
        leg_offset = 0
        if state == PetState.WALKING:
            leg_offset = math.sin(frame * math.pi) * 4
        painter.setBrush(QBrush(self.body_color))
        painter.drawRoundedRect(QRectF(-18, body_y + body_h - 5 + leg_offset, 10, 12), 3, 3)
        painter.drawRoundedRect(QRectF(8, body_y + body_h - 5 - leg_offset, 10, 12), 3, 3)

        # ===== 头部 / Head =====
        head_r = 26
        head_y = body_y - 18

        # 耳朵 / Ears
        ear_tilt = 0
        if state == PetState.SAD:
            ear_tilt = 20
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#E08A3C"), 1.5))
        # 左耳 / Left ear
        painter.save()
        painter.translate(-16, head_y - 8)
        painter.rotate(-25 + ear_tilt)
        painter.drawPolygon(*[
            Qt.QPoint(-8, 0), Qt.QPoint(0, -20), Qt.QPoint(8, 0)
        ])
        painter.restore()
        # 右耳 / Right ear
        painter.save()
        painter.translate(16, head_y - 8)
        painter.rotate(25 - ear_tilt)
        painter.drawPolygon(*[
            Qt.QPoint(-8, 0), Qt.QPoint(0, -20), Qt.QPoint(8, 0)
        ])
        painter.restore()
        # 耳朵内部 / Inner ear
        painter.setBrush(QBrush(self.ear_color))
        painter.setPen(Qt.NoPen)
        painter.save()
        painter.translate(-16, head_y - 8)
        painter.rotate(-25 + ear_tilt)
        painter.drawPolygon(*[
            Qt.QPoint(-4, -2), Qt.QPoint(0, -13), Qt.QPoint(4, -2)
        ])
        painter.restore()
        painter.save()
        painter.translate(16, head_y - 8)
        painter.rotate(25 - ear_tilt)
        painter.drawPolygon(*[
            Qt.QPoint(-4, -2), Qt.QPoint(0, -13), Qt.QPoint(4, -2)
        ])
        painter.restore()

        # 脸 / Face
        painter.setBrush(QBrush(self.body_color))
        painter.setPen(QPen(QColor("#E08A3C"), 1.5))
        painter.drawEllipse(QRectF(-head_r, head_y - head_r, head_r * 2, head_r * 2))

        # 眼睛 / Eyes
        eye_y = head_y - 3
        if state == PetState.SLEEPING:
            # 闭眼 / Closed eyes
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-14, eye_y - 4, 10, 8), 0 * 16, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 4, 10, 8), 0 * 16, 180 * 16)
        elif state == PetState.HAPPY or state == PetState.PLAYING:
            # 开心眯眼 / Happy squint
            painter.setPen(QPen(QColor("#333"), 2))
            painter.drawArc(QRectF(-14, eye_y - 2, 10, 8), 180 * 16, 180 * 16)
            painter.drawArc(QRectF(4, eye_y - 2, 10, 8), 180 * 16, 180 * 16)
        else:
            # 正常眼睛 / Normal eyes
            painter.setBrush(QBrush(QColor("#2C3E50")))
            painter.setPen(Qt.NoPen)
            blink = (frame == 0)  # 偶尔眨眼 / Occasional blink
            if blink:
                painter.setPen(QPen(QColor("#333"), 1.5))
                painter.drawLine(-14, eye_y, -4, eye_y)
                painter.drawLine(4, eye_y, 14, eye_y)
            else:
                eye_r = 5 if state == PetState.CURIOUS else 4
                painter.drawEllipse(QRectF(-12 - eye_r/2, eye_y - eye_r, eye_r, eye_r * 2))
                painter.drawEllipse(QRectF(6 - eye_r/2, eye_y - eye_r, eye_r, eye_r * 2))
                # 高光 / Highlights
                painter.setBrush(QBrush(QColor("white")))
                painter.drawEllipse(QRectF(-11, eye_y - 3, 2, 2))
                painter.drawEllipse(QRectF(7, eye_y - 3, 2, 2))

        # 鼻子 / Nose
        painter.setBrush(QBrush(QColor("#FF6B9D")))
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(*[
            Qt.QPoint(-3, eye_y + 6), Qt.QPoint(3, eye_y + 6), Qt.QPoint(0, eye_y + 10)
        ])

        # 嘴巴 / Mouth
        painter.setPen(QPen(QColor("#333"), 1.5))
        if state == PetState.EATING:
            painter.drawArc(QRectF(-5, eye_y + 8, 10, 8), 0, 180 * 16)
        elif state == PetState.HAPPY or state == PetState.PLAYING:
            painter.drawArc(QRectF(-6, eye_y + 7, 12, 8), 0, 180 * 16)
        elif state == PetState.SAD:
            painter.drawArc(QRectF(-5, eye_y + 12, 10, 6), 180 * 16, 180 * 16)
        else:
            painter.drawLine(0, eye_y + 10, -4, eye_y + 13)
            painter.drawLine(0, eye_y + 10, 4, eye_y + 13)

        # 胡须 / Whiskers
        painter.setPen(QPen(QColor("#999"), 1))
        for i in range(3):
            y_off = eye_y + 7 + i * 3
            painter.drawLine(-10, y_off, -25, y_off - 2 + i * 2)
            painter.drawLine(10, y_off, 25, y_off - 2 + i * 2)

        # 睡觉Z / Sleep Z's
        if state == PetState.SLEEPING:
            painter.setPen(QPen(QColor("#74B9FF"), 2))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            z_off = frame * 3
            painter.drawText(20, head_y - 25 - z_off, "z")
            painter.drawText(28, head_y - 35 - z_off, "Z")

        # 开心特效 / Happy effect
        if state == PetState.HAPPY or state == PetState.PLAYING:
            painter.setPen(QPen(QColor("#FFD93D"), 2))
            for angle in [0, 60, 120, 180, 240, 300]:
                rad = math.radians(angle + frame * 30)
                sx = math.cos(rad) * 35
                sy = head_y + math.sin(rad) * 30 - 10
                painter.drawText(int(sx) - 3, int(sy), "✦")

        painter.restore()

    def get_bounding_size(self, scale: float = 1.0):
        return (int(90 * scale), int(95 * scale))
