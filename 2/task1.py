import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton
from PyQt5 import uic

class FlagApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task1.ui', self) # Загрузка интерфейса из XML
        self.btn_draw.clicked.connect(self.draw_flag)

    def draw_flag(self):
        colors = []
        # Проходим по всем 3 группам (groupBox_1, groupBox_2, groupBox_3)
        for group in (self.groupBox_1, self.groupBox_2, self.groupBox_3):
            # Ищем выбранный RadioButton внутри группы
            for rb in group.findChildren(QRadioButton):
                if rb.isChecked():
                    colors.append(rb.text())
                    break
        
        self.result_label.setText(f"Выбранные цвета: {', '.join(colors)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlagApp()
    ex.show()
    sys.exit(app.exec_())