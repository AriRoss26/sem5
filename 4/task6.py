import sys
import sqlite3
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic

def init_db():
    con = sqlite3.connect('library.sqlite')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, login TEXT UNIQUE, pass_hash TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, genre TEXT, image_path TEXT)''')
    con.commit()
    con.close()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class BookForm(QDialog):
    def __init__(self, book_id=None):
        super().__init__()
        uic.loadUi('task6_form.ui', self)
        self.book_id = book_id
        self.con = sqlite3.connect('library.sqlite')
        self.img_path = ""
        
        if self.book_id:
            data = self.con.cursor().execute("SELECT * FROM books WHERE id=?", (self.book_id,)).fetchone()
            self.inp_title.setText(data[1])
            self.inp_author.setText(data[2])
            self.inp_year.setValue(data[3])
            self.inp_genre.setText(data[4])
            self.img_path = data[5]
            if self.img_path:
                self.btn_img.setText("Файл выбран")

        self.btn_img.clicked.connect(self.select_image)
        self.btn_save.clicked.connect(self.save_data)

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать обложку", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.img_path = path
            self.btn_img.setText("Файл выбран")

    def save_data(self):
        t = self.inp_title.text()
        a = self.inp_author.text()
        y = self.inp_year.value()
        g = self.inp_genre.text()
        
        if not t or not a:
            QMessageBox.warning(self, "Ошибка", "Заполните название и автора!")
            return
            
        cur = self.con.cursor()
        if self.book_id:
            cur.execute("UPDATE books SET title=?, author=?, year=?, genre=?, image_path=? WHERE id=?", (t, a, y, g, self.img_path, self.book_id))
        else:
            cur.execute("INSERT INTO books (title, author, year, genre, image_path) VALUES (?, ?, ?, ?, ?)", (t, a, y, g, self.img_path))
        self.con.commit()
        self.accept()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task6_main.ui', self)
        self.con = sqlite3.connect('library.sqlite')
        
        self.load_table()
        self.btn_search.clicked.connect(self.load_table)
        self.btn_add.clicked.connect(self.add_book)
        self.btn_edit.clicked.connect(self.edit_book)
        self.btn_del.clicked.connect(self.del_book)
        self.table.itemSelectionChanged.connect(self.show_image)

    def load_table(self):
        cur = self.con.cursor()
        query = "SELECT id, title, author, year, genre, image_path FROM books"
        
        search_text = self.inp_search.text().strip()
        if search_text:
            if self.combo_search.currentIndex() == 0: # По автору
                query += f" WHERE author LIKE '%{search_text}%'"
            else: # По названию
                query += f" WHERE title LIKE '%{search_text}%'"
                
        result = cur.fetchall() if cur.execute(query) else []
        
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Год", "Жанр"])
        self.table.setRowCount(len(result))
        
        self.books_data = {} # Храним пути к картинкам
        
        for row, data in enumerate(result):
            self.books_data[data[0]] = data[5] # id -> image_path
            for col in range(5):
                self.table.setItem(row, col, QTableWidgetItem(str(data[col])))

    def show_image(self):
        selected = self.table.selectedItems()
        if not selected: return
        
        book_id = int(self.table.item(selected[0].row(), 0).text())
        img_path = self.books_data.get(book_id, "")
        
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            self.lbl_image.setText("НЕТ ОБЛОЖКИ\n(Стандартное изображение)")
        else:
            self.lbl_image.setPixmap(pixmap.scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def add_book(self):
        if BookForm().exec_(): self.load_table()

    def edit_book(self):
        sel = self.table.selectedItems()
        if sel and BookForm(int(self.table.item(sel[0].row(), 0).text())).exec_():
            self.load_table()

    def del_book(self):
        sel = self.table.selectedItems()
        if sel and QMessageBox.question(self, "?", "Удалить?") == QMessageBox.Yes:
            self.con.cursor().execute("DELETE FROM books WHERE id=?", (int(self.table.item(sel[0].row(), 0).text()),))
            self.con.commit()
            self.load_table()

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        init_db()
        uic.loadUi('task6_auth.ui', self)
        self.con = sqlite3.connect('library.sqlite')
        
        self.btn_login.clicked.connect(self.login)
        self.btn_reg.clicked.connect(self.register)

    def login(self):
        l, p = self.inp_login.text(), self.inp_pass.text()
        user = self.con.cursor().execute("SELECT pass_hash FROM users WHERE login=?", (l,)).fetchone()
        
        if user and user[0] == hash_password(p):
            self.main_win = MainWindow()
            self.main_win.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

    def register(self):
        l, p = self.inp_login.text(), self.inp_pass.text()
        if not l or not p:
            QMessageBox.warning(self, "Ошибка", "Заполните поля!")
            return
            
        try:
            self.con.cursor().execute("INSERT INTO users (login, pass_hash) VALUES (?, ?)", (l, hash_password(p)))
            self.con.commit()
            QMessageBox.information(self, "Успех", "Вы зарегистрированы! Теперь войдите.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Логин уже занят!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AuthWindow()
    ex.show()
    sys.exit(app.exec_())