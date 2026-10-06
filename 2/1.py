import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QRadioButton, QPushButton, QLabel, QGroupBox, QButtonGroup)

class FlagApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Текстовый флаг')
        # Фиксированный размер окна (по условию)
        self.setFixedSize(400, 250)
        main_layout = QVBoxLayout()
        colors_layout = QHBoxLayout()
        self.groups = []
        self.button_groups = []
        colors = ['Красный', 'Зелёный', 'Белый', 'Синий']
        # Создаем 3 группы для трех полос
        for i in range(3):
            group_box = QGroupBox(f'Полоса {i+1}')
            vbox = QVBoxLayout()
            btn_group = QButtonGroup(self)
            for j, color in enumerate(colors):
                rb = QRadioButton(color)
                if j == 0: rb.setChecked(True) # По умолчанию выбран первый
                vbox.addWidget(rb)
                btn_group.addButton(rb)  
            group_box.setLayout(vbox)
            colors_layout.addWidget(group_box)
            self.button_groups.append(btn_group)
        main_layout.addLayout(colors_layout)
        self.btn_draw = QPushButton('Нарисовать')
        self.btn_draw.clicked.connect(self.draw_flag)
        main_layout.addWidget(self.btn_draw)
        self.result_label = QLabel('Выберите цвета и нажмите "Нарисовать"')
        main_layout.addWidget(self.result_label)
        self.setLayout(main_layout)
    def draw_flag(self):
        selected_colors = []
        for bg in self.button_groups:
            selected_colors.append(bg.checkedButton().text())
        result_text = f"Выбранные цвета: {', '.join(selected_colors)}"
        self.result_label.setText(result_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlagApp()
    ex.show()
    sys.exit(app.exec_())