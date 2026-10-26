import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic

class UFOApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task5.ui', self)
        
        self.step = 20 # Шаг перемещения
        
        # Загружаем картинку НЛО (если её нет, останется текст)
        pixmap = QPixmap('ufo.png')
        if not pixmap.isNull():
            self.ufo_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        x = self.ufo_label.x()
        y = self.ufo_label.y()
        w = self.ufo_label.width()
        h = self.ufo_label.height()

        if event.key() == Qt.Key_Left:
            x -= self.step
        elif event.key() == Qt.Key_Right:
            x += self.step
        elif event.key() == Qt.Key_Up:
            y -= self.step
        elif event.key() == Qt.Key_Down:
            y += self.step
            
        # Логика появления с другой стороны (Wrap-around)
        if x < -w: x = self.width()
        elif x > self.width(): x = -w
        
        if y < -h: y = self.height()
        elif y > self.height(): y = -h

        self.ufo_label.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UFOApp()
    ex.show()
    sys.exit(app.exec_())