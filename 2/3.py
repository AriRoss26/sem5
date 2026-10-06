import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QListWidget, QLabel)

class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Записная книжка')
        self.resize(300, 400)
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя контакта")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Номер телефона")
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_contact)
        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Телефон:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        if name and phone:
            self.list_widget.addItem(f"{name} — {phone}")
            self.name_input.clear()
            self.phone_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddressBook()
    ex.show()
    sys.exit(app.exec_())