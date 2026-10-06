import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QCalendarWidget, QTimeEdit, QLineEdit, QPushButton, QListWidget)
from PyQt5.QtCore import QTime

class PlannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Ежедневник')
        self.resize(500, 400)
        main_layout = QVBoxLayout()
        # Виджеты ввода
        input_layout = QHBoxLayout()
        self.event_input = QLineEdit()
        self.event_input.setPlaceholderText("Название события...")
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.btn_add = QPushButton('Добавить')
        self.btn_add.clicked.connect(self.add_event)
        input_layout.addWidget(self.event_input)
        input_layout.addWidget(self.time_edit)
        input_layout.addWidget(self.btn_add)
        # Календарь
        self.calendar = QCalendarWidget()
        # Список событий
        self.list_widget = QListWidget()
        main_layout.addWidget(self.calendar)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.list_widget)
        self.setLayout(main_layout)
    def add_event(self):
        event_name = self.event_input.text()
        if not event_name:
            return
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        time = self.time_edit.time().toString("HH:mm")
        # Формат yyyy-MM-dd HH:mm позволяет сортировать строки в алфавитном порядке, 
        # что будет соответствовать хронологическому порядку (по возрастанию даты)
        event_str = f"{date} {time} - {event_name}"
        self.list_widget.addItem(event_str)
        self.list_widget.sortItems() # Автоматическая сортировка списка
        self.event_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlannerApp()
    ex.show()
    sys.exit(app.exec_())