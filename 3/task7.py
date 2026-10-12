import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl
from PyQt5 import uic

class PianoApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task7.ui', self)
        
        self.setup_key(self.btn_do, 'do.wav')
        self.setup_key(self.btn_re, 're.wav')
        self.setup_key(self.btn_mi, 'mi.wav')
        self.setup_key(self.btn_fa, 'fa.wav')

    def setup_key(self, button, filename):
        effect = QSoundEffect(self)
        
        path = os.path.join(os.getcwd(), filename)
        if os.path.exists(path):
            effect.setSource(QUrl.fromLocalFile(path))
            button.clicked.connect(effect.play)
        else:
            button.clicked.connect(lambda: QMessageBox.warning(self, "Ошибка", f"Файл {filename} не найден!"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PianoApp()
    ex.show()
    sys.exit(app.exec_())