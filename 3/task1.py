import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5 import uic

class StatsApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task1.ui', self)
        
        self.btn_load.clicked.connect(self.load_file)
        self.btn_save.clicked.connect(self.save_file)
        
        self.stats = None

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите текстовый файл", "", "Text Files (*.txt)")
        if not filename: return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            numbers = [int(x) for x in content.split()]
            
            if not numbers:
                raise ValueError("Файл пуст или не содержит чисел.")

            max_val = max(numbers)
            min_val = min(numbers)
            avg_val = sum(numbers) / len(numbers)

            self.stats = (max_val, min_val, avg_val)
            self.lbl_max.setText(f"Максимальное: {max_val}")
            self.lbl_min.setText(f"Минимальное: {min_val}")
            self.lbl_avg.setText(f"Среднее: {avg_val:.2f}")
            self.btn_save.setEnabled(True)

        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Файл содержит неверный формат данных (ожидаются только целые числа).")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл:\n{e}")

    def save_file(self):
        if not self.stats: return
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt)")
        if not filename: return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Максимальное: {self.stats[0]}\n")
                f.write(f"Минимальное: {self.stats[1]}\n")
                f.write(f"Среднее: {self.stats[2]:.2f}\n")
            QMessageBox.information(self, "Успех", "Данные успешно сохранены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StatsApp()
    ex.show()
    sys.exit(app.exec_())