import sys
import sqlite3
import datetime
import os
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QMessageBox
from PyQt5 import uic

class FilmForm(QDialog):
    def __init__(self, film_id=None):
        super().__init__()
        uic.loadUi('task2_form.ui', self)
        self.film_id = film_id
        
        # Подключаемся к существующей БД
        self.con = sqlite3.connect('films_db.sqlite')
        
        self.load_genres()
        
        if self.film_id:
            self.load_film_data()
            
        self.btn_save.clicked.connect(self.save_data)

    def load_genres(self):
        try:
            genres = self.con.cursor().execute("SELECT id, title FROM genres").fetchall()
            for g_id, title in genres:
                self.combo_genre.addItem(title, g_id) # Сохраняем ID жанра невидимым параметром
        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось загрузить жанры:\n{e}")

    def load_film_data(self):
        try:
            data = self.con.cursor().execute("SELECT title, year, genre, duration FROM films WHERE id = ?", (self.film_id,)).fetchone()
            if data:
                self.inp_title.setText(str(data[0]))
                self.inp_year.setValue(int(data[1]))
                self.inp_duration.setValue(int(data[3]))
                
                # Ищем нужный жанр в выпадающем списке и выбираем его
                idx = self.combo_genre.findData(data[2])
                if idx >= 0:
                    self.combo_genre.setCurrentIndex(idx)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось загрузить данные фильма:\n{e}")

    def save_data(self):
        title = self.inp_title.text().strip()
        year = self.inp_year.value()
        duration = self.inp_duration.value()
        genre_id = self.combo_genre.currentData()

        # Валидация по заданию
        if not title:
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым!")
            return
        if duration <= 0:
            QMessageBox.warning(self, "Ошибка", "Длина (продолжительность) должна быть положительным числом!")
            return
        if year > datetime.datetime.now().year:
            QMessageBox.warning(self, "Ошибка", "Год не может быть в будущем!")
            return

        try:
            cur = self.con.cursor()
            if self.film_id:
                cur.execute("UPDATE films SET title=?, year=?, genre=?, duration=? WHERE id=?", 
                            (title, year, genre_id, duration, self.film_id))
            else:
                cur.execute("INSERT INTO films (title, year, genre, duration) VALUES (?, ?, ?, ?)", 
                            (title, year, genre_id, duration))
            
            self.con.commit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось сохранить данные:\n{e}")

class FilmApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # СТРОГАЯ ПРОВЕРКА: существует ли файл БД от преподавателя?
        if not os.path.exists('films_db.sqlite'):
            app = QApplication.instance()
            QMessageBox.critical(None, "Критическая ошибка", 
                                 "Файл 'films_db.sqlite' не найден в папке с программой!\n"
                                 "Пожалуйста, скачайте файл по ссылке, убедитесь, что он называется "
                                 "именно так (без цифр), и положите его рядом со скриптом.")
            sys.exit(1)
            
        uic.loadUi('task2_main.ui', self)
        
        self.con = sqlite3.connect('films_db.sqlite')
        
        self.btn_add.clicked.connect(self.add_film)
        self.btn_edit.clicked.connect(self.edit_film)
        self.btn_del.clicked.connect(self.del_film)
        
        self.load_table()

    def load_table(self):
        try:
            cur = self.con.cursor()
            # Запрос объединяет таблицы, чтобы вместо цифры жанра вывести его текст
            query = """SELECT films.id AS 'ID', films.title AS 'Название', films.year AS 'Год', 
                              genres.title AS 'Жанр', films.duration AS 'Длина (мин)' 
                       FROM films 
                       LEFT JOIN genres ON films.genre = genres.id"""
            
            result = cur.execute(query).fetchall()
            
            # Получаем названия столбцов динамически из БД (как требует задание)
            headers = [description[0] for description in cur.description]
            
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.table.setRowCount(len(result))
            
            for row_idx, row_data in enumerate(result):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
                    
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Структура БД не совпадает с ожидаемой. Ошибка:\n{e}")

    def add_film(self):
        if FilmForm().exec_():
            self.load_table()

    def edit_film(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Сначала выделите строку в таблице для редактирования!")
            return
        
        row = selected[0].row()
        film_id = int(self.table.item(row, 0).text())
        
        if FilmForm(film_id).exec_():
            self.load_table()

    def del_film(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Сначала выделите строку в таблице для удаления!")
            return
            
        row = selected[0].row()
        film_id = int(self.table.item(row, 0).text())
        film_title = self.table.item(row, 1).text()
        
        ans = QMessageBox.question(self, "Удаление", f"Вы уверены, что хотите удалить фильм '{film_title}'?", 
                                   QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            try:
                self.con.cursor().execute("DELETE FROM films WHERE id = ?", (film_id,))
                self.con.commit()
                self.load_table()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить фильм:\n{e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FilmApp()
    ex.show()
    sys.exit(app.exec_())