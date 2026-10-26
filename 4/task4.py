import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic

class RunawayApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task4.ui', self)
        
        # Перехватываем событие наведения мыши на кнопку
        self.btn_runaway.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Если событие произошло на нашей кнопке и это событие "Наведение курсора" (Enter)
        if obj == self.btn_runaway and event.type() == event.Enter:
            self.move_button()
            return True
        return super().eventFilter(obj, event)

    def move_button(self):
        # Вычисляем безопасные границы, чтобы кнопка не улетела за экран
        max_x = self.width() - self.btn_runaway.width()
        max_y = self.height() - self.btn_runaway.height()
        
        new_x = random.randint(0, max_x)
        new_y = random.randint(0, max_y)
        
        self.btn_runaway.move(new_x, new_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RunawayApp()
    ex.show()
    sys.exit(app.exec_())