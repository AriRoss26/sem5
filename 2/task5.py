import sys
import difflib # Встроенная библиотека Python для сравнения последовательностей
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class AntiPlagiarism(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task5.ui', self)
        
        self.statusbar.showMessage("Готово к проверке")
        self.btn_check.clicked.connect(self.check_plagiarism)

    def check_plagiarism(self):
        # Получаем тексты из полей целиком (удаляя только лишние пробелы по краям)
        text1 = self.text1.toPlainText().strip()
        text2 = self.text2.toPlainText().strip()

        if not text1 or not text2:
            self.statusbar.setStyleSheet("color: black;")
            self.statusbar.showMessage("Ошибка: Одно или оба поля пусты.")
            return

        # Используем SequenceMatcher для умного вычисления процента сходства текстов
        # Он ищет общие подстроки, игнорируя мелкие различия
        matcher = difflib.SequenceMatcher(None, text1, text2)
        similarity = matcher.ratio() * 100 # ratio() возвращает число от 0.0 до 1.0

        threshold = self.threshold_spin.value()

        if similarity >= threshold:
            self.statusbar.setStyleSheet("color: red; font-weight: bold;")
            msg = f"Плагиат обнаружен! Сходство: {similarity:.1f}% (Порог: {threshold}%)"
        else:
            self.statusbar.setStyleSheet("color: green; font-weight: bold;")
            msg = f"Текст оригинален. Сходство: {similarity:.1f}% (Порог: {threshold}%)"

        self.statusbar.showMessage(msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AntiPlagiarism()
    ex.show()
    sys.exit(app.exec_())