import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import uic

class DrawingApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task3.ui', self)
        self.shapes = [] # Хранит кортежи: (тип, x, y, размер, цвет)
        # Включаем отслеживание мыши, чтобы пробел знал, где курсор
        self.setMouseTracking(True) 
        self.cursor_pos = QPoint(0, 0)

    def mouseMoveEvent(self, event):
        self.cursor_pos = event.pos()

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        size = random.randint(20, 100)
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        if event.button() == Qt.LeftButton:
            self.shapes.append(('circle', x, y, size, color))
        elif event.button() == Qt.RightButton:
            self.shapes.append(('square', x, y, size, color))
            
        self.update() # Перерисовка

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            x, y = self.cursor_pos.x(), self.cursor_pos.y()
            size = random.randint(20, 100)
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.shapes.append(('triangle', x, y, size, color))
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape, x, y, size, color in self.shapes:
            painter.setBrush(color)
            if shape == 'circle':
                painter.drawEllipse(x - size//2, y - size//2, size, size)
            elif shape == 'square':
                painter.drawRect(x - size//2, y - size//2, size, size)
            elif shape == 'triangle':
                points = QPolygon([
                    QPoint(x, y - size), 
                    QPoint(x - size, y + size), 
                    QPoint(x + size, y + size)
                ])
                painter.drawPolygon(points)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DrawingApp()
    ex.show()
    sys.exit(app.exec_())