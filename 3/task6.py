import sys
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5 import uic

class SmileyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task6.ui', self)
        
        self.color = QColorDialog.getColor()
        if not self.color.isValid():
            self.color = Qt.yellow

        self.slider_scale.valueChanged.connect(self.draw_smiley)
        self.draw_smiley()

    def draw_smiley(self):
        size = 350
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        scale = self.slider_scale.value() / 100.0
        
        painter.translate(size/2, size/2)
        painter.scale(scale, scale)
        
        painter.setBrush(self.color)
        painter.drawEllipse(-100, -100, 200, 200)
        
        painter.setBrush(Qt.black)
        painter.drawEllipse(-40, -40, 20, 20)
        painter.drawEllipse(20, -40, 20, 20)
        
        pen = QPen(Qt.black, 5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(-50, -20, 100, 80, 180 * 16, 180 * 16)
        
        painter.end()
        self.lbl_canvas.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmileyApp()
    ex.show()
    sys.exit(app.exec_())