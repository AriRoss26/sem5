import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5 import uic

class OlympiadResults(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task1.ui', self)
        
        self.data = [] # Храним все распарсенные данные
        self.schools = set()
        self.classes = set()
        
        self.load_data()
        self.setup_filters()
        
        self.combo_school.currentIndexChanged.connect(self.update_table)
        self.combo_class.currentIndexChanged.connect(self.update_table)
        
        self.update_table()

    def load_data(self):
        try:
            with open('results.csv', 'r', encoding='utf-8') as f:
                # Пропускаем заголовок
                next(f)
                for line in f:
                    # Разделяем по запятым, убираем кавычки
                    parts = [p.strip('" \n') for p in line.split(',')]
                    if len(parts) >= 8:
                        login = parts[2]
                        name = parts[1]
                        score = int(parts[7])
                        
                        # Парсинг логина sh-kaluga16-**-##-@
                        login_parts = login.split('-')
                        if len(login_parts) >= 5:
                            school = login_parts[2]
                            cls = login_parts[3]
                            
                            self.data.append({'login': login, 'name': name, 'score': score, 'school': school, 'class': cls})
                            self.schools.add(school)
                            self.classes.add(cls)
        except Exception as e:
            print(f"Ошибка чтения файла (убедитесь, что results.csv рядом со скриптом): {e}")

    def setup_filters(self):
        self.combo_school.addItem("Все")
        self.combo_school.addItems(sorted(list(self.schools)))
        
        self.combo_class.addItem("Все")
        self.combo_class.addItems(sorted(list(self.classes)))

    def update_table(self):
        sel_school = self.combo_school.currentText()
        sel_class = self.combo_class.currentText()
        
        # Фильтрация
        filtered = []
        for d in self.data:
            if sel_school != "Все" and d['school'] != sel_school:
                continue
            if sel_class != "Все" and d['class'] != sel_class:
                continue
            filtered.append(d)
            
        # Находим топ-3 уникальных балла для окрашивания
        unique_scores = sorted(list(set(d['score'] for d in filtered)), reverse=True)
        top_scores = unique_scores[:3] if len(unique_scores) >= 3 else unique_scores

        self.tableWidget.setRowCount(len(filtered))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Логин", "ФИО", "Балл"])
        
        colors = {
            0: QColor(255, 215, 0),    # Золото (1 место)
            1: QColor(192, 192, 192),  # Серебро (2 место)
            2: QColor(205, 127, 50)    # Бронза (3 место)
        }

        for row, d in enumerate(filtered):
            i_log = QTableWidgetItem(d['login'])
            i_name = QTableWidgetItem(d['name'])
            i_score = QTableWidgetItem(str(d['score']))
            
            # Окрашивание
            if d['score'] in top_scores:
                place_idx = top_scores.index(d['score'])
                color = colors[place_idx]
                i_log.setBackground(color); i_name.setBackground(color); i_score.setBackground(color)

            self.tableWidget.setItem(row, 0, i_log)
            self.tableWidget.setItem(row, 1, i_name)
            self.tableWidget.setItem(row, 2, i_score)
            
        self.tableWidget.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OlympiadResults()
    ex.show()
    sys.exit(app.exec_())