import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5 import uic

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task2.ui', self)
        
        self.btn_new.clicked.connect(self.new_file)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить", "", "Text Files (*.txt);;All Files (*)")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec_())