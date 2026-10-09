import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic

class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task3.ui', self)
        self.btn_add.clicked.connect(self.add_contact)

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