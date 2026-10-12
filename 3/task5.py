import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5 import uic

class FlagGenerator(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task5.ui', self)
        
        num_colors, ok = QInputDialog.getInt(self, "Количество цветов", "Введите количество полос флага:", 3, 1, 20)
        
        if ok and num_colors > 0:
            self.generate_flag(num_colors)
        else:
            sys.exit()

    def generate_flag(self, num_colors):
        width = 500
        height = 300
        pixmap = QPixmap(width, height)
        painter = QPainter(pixmap)
        
        stripe_height = height / num_colors
        
        for i in range(num_colors):
            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            painter.fillRect(0, int(i * stripe_height), width, int(stripe_height + 1), color)
            
        painter.end()
        self.lbl_flag.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlagGenerator()
    ex.show()
    sys.exit(app.exec_())