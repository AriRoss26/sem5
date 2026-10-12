import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt
from PyQt5 import uic

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task3.ui', self)
        
        self.original_image = QImage()
        self.current_angle = 0
        self.current_channel = 'ALL'

        self.btn_rot_left.clicked.connect(lambda: self.rotate(-90))
        self.btn_rot_right.clicked.connect(lambda: self.rotate(90))
        
        self.rb_all.toggled.connect(lambda: self.change_channel('ALL'))
        self.rb_red.toggled.connect(lambda: self.change_channel('R'))
        self.rb_green.toggled.connect(lambda: self.change_channel('G'))
        self.rb_blue.toggled.connect(lambda: self.change_channel('B'))

        self.load_image()

    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.original_image = QImage(filename)
            self.apply_transformations()

    def rotate(self, angle):
        self.current_angle = (self.current_angle + angle) % 360
        self.apply_transformations()

    def change_channel(self, channel):
        self.current_channel = channel
        self.apply_transformations()

    def apply_transformations(self):
        if self.original_image.isNull(): return

        img = self.original_image.copy()
        
        if self.current_channel != 'ALL':
            for y in range(img.height()):
                for x in range(img.width()):
                    color = img.pixelColor(x, y)
                    if self.current_channel == 'R':
                        color.setGreen(0); color.setBlue(0)
                    elif self.current_channel == 'G':
                        color.setRed(0); color.setBlue(0)
                    elif self.current_channel == 'B':
                        color.setRed(0); color.setGreen(0)
                    img.setPixelColor(x, y, color)

        transform = QTransform().rotate(self.current_angle)
        final_pixmap = QPixmap.fromImage(img).transformed(transform)
        
        scaled_pixmap = final_pixmap.scaled(750, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl_image.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageEditor()
    ex.show()
    sys.exit(app.exec_())