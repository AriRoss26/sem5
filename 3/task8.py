import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5 import uic

class LSystem(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task8.ui', self)
        
        self.name = ""
        self.angle = 90
        self.axiom = ""
        self.rules = {}
        
        self.slider_steps.valueChanged.connect(self.draw_system)
        
        self.load_file()

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите файл L-системы", "", "Text Files (*.txt)")
        if not filename:
            sys.exit()
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                
            self.name = lines[0]
            self.lbl_title.setText(self.name)
            
            self.angle = 360.0 / float(lines[1]) 
            self.axiom = lines[2]
            
            for line in lines[3:]:
                parts = line.split()
                if len(parts) >= 2:
                    self.rules[parts[0]] = parts[1]
                    
            self.draw_system()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка чтения файла:\n{e}")
            sys.exit()

    def get_string_for_iteration(self, iterations):
        result = self.axiom
        for _ in range(iterations):
            next_result = ""
            for char in result:
                next_result += self.rules.get(char, char)
            result = next_result
        return result

    def draw_system(self):
        iters = self.slider_steps.value()
        commands = self.get_string_for_iteration(iters)
        
        width = self.lbl_canvas.width() or 800
        height = self.lbl_canvas.height() or 500
        
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.white)
        
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 1))
        
        painter.translate(width / 2, height - 50) 
        
        line_length = 200 / (2 ** iters) if iters > 0 else 200
        
        for char in commands:
            if char == 'F':
                painter.drawLine(0, 0, 0, int(-line_length))
                painter.translate(0, -line_length)
            elif char == '+':
                painter.rotate(self.angle)
            elif char == '-':
                painter.rotate(-self.angle)
            elif char == '[':
                painter.save()
            elif char == ']':
                painter.restore()
                
        painter.end()
        self.lbl_canvas.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LSystem()
    ex.show()
    sys.exit(app.exec_())