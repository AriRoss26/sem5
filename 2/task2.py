import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTime
from PyQt5 import uic

class PlannerApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task2.ui', self)
        
        self.time_edit.setTime(QTime.currentTime())
        self.btn_add.clicked.connect(self.add_event)

    def add_event(self):
        event_name = self.event_input.text()
        if not event_name:
            return

        # Формат для правильной строковой сортировки (Год-Месяц-День Время)
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        time = self.time_edit.time().toString("HH:mm")
        
        event_str = f"{date} {time} - {event_name}"
        
        self.list_widget.addItem(event_str)
        self.list_widget.sortItems() # Авто-сортировка по возрастанию даты
        self.event_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlannerApp()
    ex.show()
    sys.exit(app.exec_())