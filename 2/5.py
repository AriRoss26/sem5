import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QDoubleSpinBox, QTextEdit, QPushButton, QLabel)

class AntiPlagiarism(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Антиплагиат')
        self.resize(600, 500)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        # Настройки порога
        thresh_layout = QHBoxLayout()
        thresh_layout.addWidget(QLabel("Порог срабатывания (%):"))
        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(0.0, 100.0)
        self.threshold_spin.setValue(70.0) # По умолчанию 70%
        thresh_layout.addWidget(self.threshold_spin)
        thresh_layout.addStretch()
        main_layout.addLayout(thresh_layout)
        # Текстовые поля
        texts_layout = QHBoxLayout()
        self.text1 = QTextEdit()
        self.text1.setPlaceholderText("Вставьте оригинальный текст сюда...")
        self.text2 = QTextEdit()
        self.text2.setPlaceholderText("Вставьте проверяемый текст сюда...")
        texts_layout.addWidget(self.text1)
        texts_layout.addWidget(self.text2)
        main_layout.addLayout(texts_layout)
        # Кнопка
        self.btn_check = QPushButton("Рассчитать результат")
        self.btn_check.clicked.connect(self.check_plagiarism)
        main_layout.addWidget(self.btn_check)
        central_widget.setLayout(main_layout)
        # StatusBar
        self.statusBar().showMessage("Готово к проверке")
    def check_plagiarism(self):
        # Получаем текст, разбиваем на строки, удаляем пустые и лишние пробелы
        lines1 = [line.strip() for line in self.text1.toPlainText().split('\n') if line.strip()]
        lines2 = [line.strip() for line in self.text2.toPlainText().split('\n') if line.strip()]
        if not lines1 or not lines2:
            self.statusBar().setStyleSheet("color: black;")
            self.statusBar().showMessage("Ошибка: Одно или оба поля пусты.")
            return
        # Простейший алгоритм, ищем одинаковые строки без учета их порядка
        set1 = set(lines1)
        set2 = set(lines2)
        common_lines = set1.intersection(set2)
        # Считаем процент по отношению к самому длинному тексту
        max_len = max(len(lines1), len(lines2))
        similarity = (len(common_lines) / max_len) * 100
        threshold = self.threshold_spin.value()
        if similarity >= threshold:
            self.statusBar().setStyleSheet("color: red; font-weight: bold;")
            result_msg = f"Плагиат обнаружен! Сходство: {similarity:.2f}% (Порог: {threshold}%)"
        else:
            self.statusBar().setStyleSheet("color: green; font-weight: bold;")
            result_msg = f"Текст оригинален. Сходство: {similarity:.2f}% (Порог: {threshold}%)"
        self.statusBar().showMessage(result_msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AntiPlagiarism()
    ex.show()
    sys.exit(app.exec_())