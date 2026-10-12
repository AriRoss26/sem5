import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

class TransparencyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task4.ui', self)
        
        self.btn_load.clicked.connect(self.load_image)
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.lbl_image.setGraphicsEffect(self.opacity_effect)
        
        self.slider_alpha.valueChanged.connect(self.change_opacity)

    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            pixmap = QPixmap(filename)
            self.lbl_image.setPixmap(pixmap.scaled(self.lbl_image.size(), 1, 1))

    def change_opacity(self, value):
        self.opacity_effect.setOpacity(value / 100.0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TransparencyApp()
    ex.show()
    sys.exit(app.exec_())