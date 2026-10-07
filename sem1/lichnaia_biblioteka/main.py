import sys
import os
import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from database import DatabaseManager
from ui_main import Ui_MainWindow
from ui_dialog import Ui_BookDialog

# Константы
SOUND_DELETE = "delete.wav"
DEFAULT_COVER = "default_cover.jpg"

class BookDialog(QtWidgets.QDialog, Ui_BookDialog):
    """Класс диалогового окна добавления/редактирования книги."""
    
    def __init__(self, db_manager, book_data=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db_manager = db_manager
        self.book_data = book_data  # None если создание, tuple если редактирование
        
        self.genre_mapping = {} # Для связи имени жанра и его ID
        self.load_genres()
        self.setup_connections()
        
        if self.book_data:
            self.fill_data()

    def load_genres(self):
        """Загружает жанры из БД в ComboBox."""
        genres = self.db_manager.get_all_genres()
        for genre_id, name in genres:
            self.cb_genre.addItem(name)
            self.genre_mapping[name] = genre_id

    def setup_connections(self):
        """Подключает сигналы к слотам."""
        self.btn_browse.clicked.connect(self.browse_image)

    def fill_data(self):
        """Заполняет поля диалога данными при редактировании."""
        self.le_title.setText(self.book_data[1])
        self.le_author.setText(self.book_data[2])
        self.le_year.setText(str(self.book_data[3]))
        
        genre_name = self.book_data[4]
        index = self.cb_genre.findText(genre_name)
        if index >= 0:
            self.cb_genre.setCurrentIndex(index)
            
        cover = self.book_data[5]
        if cover:
            self.le_cover_path.setText(cover)

    def browse_image(self):
        """Стандартный диалог выбора файла (обложки)."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберите обложку", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.le_cover_path.setText(file_name)

    def get_data(self):
        """Возвращает введенные пользователем данные с полной проверкой."""
        title = self.le_title.text().strip()
        author = self.le_author.text().strip()
        year_str = self.le_year.text().strip()
        genre_name = self.cb_genre.currentText()
        genre_id = self.genre_mapping.get(genre_name)
        cover_path = self.le_cover_path.text().strip()
        
        # 1. Проверка на пустые поля
        if not title:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите название книги!")
            return None
        if not author:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите автора книги!")
            return None

        # 2. Проверка года
        current_year = datetime.datetime.now().year
        if not year_str:
            year = 0  # Если оставили пустым, ставим 0
        else:
            try:
                year = int(year_str)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Год должен состоять только из цифр!")
                return None

        # Проверка диапазона года
        if year < 0 or year > current_year:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Год должен быть в диапазоне от 0 до {current_year}!")
            return None
            
        # 3. Гарантированный возврат всех данных кортежем
        return (title, author, year, genre_id, cover_path)


class LibraryApp(QtWidgets.QMainWindow, Ui_MainWindow):
    """Главный класс приложения."""
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = DatabaseManager()
        
        # Настройка таблицы
        self.tableWidget.setColumnHidden(0, True) # Скрываем колонку ID от пользователя
        
        self.setup_connections()
        self.load_data()

    def setup_connections(self):
        """Подключает обработчики событий интерфейса."""
        self.btn_add.clicked.connect(self.add_book)
        self.btn_edit.clicked.connect(self.edit_book)
        self.btn_delete.clicked.connect(self.delete_book)
        self.tableWidget.itemSelectionChanged.connect(self.display_cover)

    def load_data(self):
        """Загружает данные из БД в таблицу."""
        self.tableWidget.setRowCount(0)
        books = self.db.get_all_books()
        
        for row_idx, book in enumerate(books):
            self.tableWidget.insertRow(row_idx)
            for col_idx, data in enumerate(book[:5]): # Первые 5 полей для таблицы
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_idx, col_idx, item)
            
            # Сохраняем путь к обложке в скрытых данных первой ячейки
            self.tableWidget.item(row_idx, 0).setData(QtCore.Qt.UserRole, book[5])

    def display_cover(self):
        """Отображает обложку выбранной книги (Мультимедиа)."""
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            self.lbl_cover.clear()
            self.lbl_cover.setText("Обложка")
            return
            
        row = selected_rows[0].row()
        cover_path = self.tableWidget.item(row, 0).data(QtCore.Qt.UserRole)
        
        if cover_path and os.path.exists(cover_path):
            # Используем QImageReader, чтобы он прочитал EXIF-данные и правильно повернул фото
            reader = QtGui.QImageReader(cover_path)
            reader.setAutoTransform(True)  # Вот эта строчка решает проблему с поворотом!
            image = reader.read()
            pixmap = QtGui.QPixmap.fromImage(image)
        else:
            # То же самое делаем для дефолтной обложки
            if os.path.exists(DEFAULT_COVER):
                reader = QtGui.QImageReader(DEFAULT_COVER)
                reader.setAutoTransform(True)
                image = reader.read()
                pixmap = QtGui.QPixmap.fromImage(image)
            else:
                self.lbl_cover.setText("Нет обложки")
                return
                
        self.lbl_cover.setPixmap(pixmap)

    def add_book(self):
        """Логика добавления новой книги через диалог."""
        dialog = BookDialog(self.db, parent=self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            if data:
                self.db.add_book(*data)
                self.load_data()

    def edit_book(self):
        """Логика редактирования выбранной книги."""
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.information(self, "Инфо", "Выберите книгу для редактирования.")
            return
            
        row = selected_rows[0].row()
        # Собираем данные из строки таблицы
        book_id = int(self.tableWidget.item(row, 0).text())
        title = self.tableWidget.item(row, 1).text()
        author = self.tableWidget.item(row, 2).text()
        year = int(self.tableWidget.item(row, 3).text())
        genre = self.tableWidget.item(row, 4).text()
        cover_path = self.tableWidget.item(row, 0).data(QtCore.Qt.UserRole)
        
        book_data = (book_id, title, author, year, genre, cover_path)
        
        dialog = BookDialog(self.db, book_data=book_data, parent=self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            if data:
                self.db.update_book(book_id, *data)
                self.load_data()

    def delete_book(self):
        """Логика удаления книги с подтверждением и звуком."""
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        book_title = self.tableWidget.item(row, 1).text()
        
        # Стандартный диалог
        reply = QtWidgets.QMessageBox.question(
            self, 'Подтверждение', 
            f"Вы уверены, что хотите удалить книгу '{book_title}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            book_id = int(self.tableWidget.item(row, 0).text())
            self.db.delete_book(book_id)
            self.load_data()
            
            # Воспроизведение звука удаления через QMediaPlayer (Мультимедиа)
            if os.path.exists(SOUND_DELETE):
                # Создаем плеер, если его еще нет
                if not hasattr(self, 'player'):
                    self.player = QMediaPlayer()
                
                # Загружаем и играем файл
                url = QtCore.QUrl.fromLocalFile(os.path.abspath(SOUND_DELETE))
                content = QMediaContent(url)
                self.player.setMedia(content)
                self.player.play()

    # --- Обработка событий мыши и клавиатуры ---
    
    def keyPressEvent(self, event):
        """Обработка нажатия клавиш клавиатуры (Удаление по Delete)."""
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_book()
        else:
            super().keyPressEvent(event)
            
    def mouseDoubleClickEvent(self, event):
        """Обработка двойного клика мыши (Редактирование по двойному клику)."""
        # Проверяем, кликнули ли мы по таблице
        child = self.childAt(event.pos())
        if child and child.parent() == self.tableWidget.viewport():
            self.edit_book()
        else:
            super().mouseDoubleClickEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion") # Красивый современный стиль
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())