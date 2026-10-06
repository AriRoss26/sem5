import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLineEdit, QPushButton, 
                             QLabel, QTabWidget, QCheckBox, QPlainTextEdit, QSpinBox)

# Задание №1: Перекидыватель слов
class Task1(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.btn = QPushButton("->")
        
        self.direction_right = True # Флаг: отслеживает текущее направление переноса
        
        layout.addWidget(self.input1)
        layout.addWidget(self.btn)
        layout.addWidget(self.input2)
        self.setLayout(layout)
        
        self.btn.clicked.connect(self.toss_word) # Привязка клика к методу
        
    def toss_word(self):
        if self.direction_right: # Перенос слева направо
            self.input2.setText(self.input1.text())
            self.input1.clear()
            self.btn.setText("<-")
        else: # Перенос справа налево
            self.input1.setText(self.input2.text())
            self.input2.clear()
            self.btn.setText("->")
        self.direction_right = not self.direction_right # Инвертируем направление

# Задание №2: Вычислитель выражений (eval)
class Task2(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.expr_input = QLineEdit()
        self.btn = QPushButton("Вычислить")
        self.result_output = QLineEdit()
        self.result_output.setReadOnly(True)
        
        layout.addWidget(self.expr_input)
        layout.addWidget(self.btn)
        layout.addWidget(self.result_output)
        self.setLayout(layout)
        
        self.btn.clicked.connect(self.calculate)
        
    def calculate(self):
        try:
            result = eval(self.expr_input.text()) # eval выполняет строку как Python-код
            self.result_output.setText(str(result))
        except Exception: # Защита от некорректного ввода
            self.result_output.setText("Ошибка в выражении")

# Задание №3: Универсальный обработчик чекбоксов
class Task3(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.widget_map = {} # Словарь для связи: чекбокс -> управляемый им виджет
        
        widgets = [QLineEdit("Текстовое поле"), QPushButton("Кнопка"), QLabel("Просто текст")]
        
        for i, widget in enumerate(widgets):
            row_layout = QHBoxLayout()
            cb = QCheckBox(f"Показать виджет {i+1}")
            cb.setChecked(True)
            
            cb.toggled.connect(self.universal_handler) # Единый метод для всех чекбоксов
            self.widget_map[cb] = widget # Сохраняем пару "чекбокс-виджет"
            
            row_layout.addWidget(cb)
            row_layout.addWidget(widget)
            layout.addLayout(row_layout)
            
        self.setLayout(layout)
        
    def universal_handler(self, checked):
        sender_checkbox = self.sender() # Получаем объект чекбокса, который был нажат
        if sender_checkbox in self.widget_map:
            self.widget_map[sender_checkbox].setVisible(checked) # Скрываем/показываем нужный виджет

# Задание №4: Азбука Морзе в цикле
class Task4(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.output = QLineEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)
        grid = QGridLayout()
        
        morse_dict = {
            'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',    'F': '..-.',
            'G': '--.',  'H': '....', 'I': '..',   'J': '.---', 'K': '-.-',  'L': '.-..',
            'M': '--',   'N': '-.',   'O': '---',  'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...',  'T': '-',    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-',
            'Y': '-.--', 'Z': '--..'
        }
        max_columns = 6
        
        for i, (letter, code) in enumerate(morse_dict.items()):
            btn = QPushButton(letter)
            # lambda c=code "замораживает" текущий код для конкретной кнопки
            btn.clicked.connect(lambda checked, c=code: self.add_morse(c))
            
            row = i // max_columns # Вычисляем номер строки в сетке
            col = i % max_columns # Вычисляем номер столбца в сетке
            grid.addWidget(btn, row, col)
            
        layout.addLayout(grid)
        btn_clear = QPushButton("Очистить")
        btn_clear.clicked.connect(self.output.clear)
        layout.addWidget(btn_clear)
        self.setLayout(layout)
        
    def add_morse(self, code):
        self.output.setText(self.output.text() + code + " ") # Дописываем символ

# Задание №5: Заказ в ресторане
class Task5(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.menu = [
            {"name": "Борщ", "price": 300},
            {"name": "булочка", "price": 80},
            {"name": "Компот", "price": 40}
        ]
        self.ui_items = [] # Список для хранения элементов интерфейса блюд
        
        for item in self.menu:
            row = QHBoxLayout()
            cb = QCheckBox(f"{item['name']} ({item['price']} руб.)")
            spinbox = QSpinBox()
            spinbox.setRange(1, 10)
            spinbox.setEnabled(False) # Счетчик заблокирован по умолчанию
            
            cb.toggled.connect(spinbox.setEnabled) # Включаем счетчик только если нажата галочка
            row.addWidget(cb)
            row.addWidget(spinbox)
            layout.addLayout(row)
            
            self.ui_items.append((cb, spinbox, item['name'], item['price'])) # Сохраняем данные для чека
            
        self.btn_order = QPushButton("Оформить заказ")
        self.btn_order.clicked.connect(self.make_order)
        self.receipt = QPlainTextEdit()
        
        layout.addWidget(self.btn_order)
        layout.addWidget(self.receipt)
        self.setLayout(layout)
        
    def make_order(self):
        text = "--- ЧЕК ---\n"
        total = 0
        for cb, spinbox, name, price in self.ui_items:
            if cb.isChecked(): # Считаем только выбранные блюда
                qty = spinbox.value()
                cost = qty * price
                text += f"{name} x {qty} = {cost} руб.\n"
                total += cost
        text += f"------------------\nИТОГО: {total} руб."
        self.receipt.setPlainText(text)

# Задание №6: Калькулятор
class Task6(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        layout.addWidget(self.display)
        
        grid = QGridLayout()
        # Данные кнопок: (текст, строка, столбец, [размах строк, размах столбцов])
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('C', 3, 0), ('0', 3, 1), ('.', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 1, 4) # Кнопка '=' занимает 4 столбца
        ]
        self.expression = ""
        
        for btn_data in buttons:
            text = btn_data[0]
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, t=text: self.on_click(t)) # Захватываем символ кнопки
            
            if len(btn_data) == 3: # Обычная кнопка
                grid.addWidget(btn, btn_data[1], btn_data[2])
            else: # Кнопка с объединением ячеек
                grid.addWidget(btn, btn_data[1], btn_data[2], btn_data[3], btn_data[4])
                
        layout.addLayout(grid)
        self.setLayout(layout)
        
    def on_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display.setText("0")
        elif char == '=':
            try:
                result = eval(self.expression)
                self.display.setText(str(result))
                self.expression = str(result)
            except ZeroDivisionError: # Обработка деления на ноль
                self.display.setText("Ошибка: деление на 0!")
                self.expression = ""
            except Exception:
                self.display.setText("Ошибка")
                self.expression = ""
        else:
            self.expression += char # Накапливаем выражение
            self.display.setText(self.expression)

# Главное окно, в котором объединяется всё во вкладках
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сборник заданий")
        tabs = QTabWidget() # Виджет вкладок
        
        tabs.addTab(Task1(), "Задание 1")
        tabs.addTab(Task2(), "Задание 2")
        tabs.addTab(Task3(), "Задание 3")
        tabs.addTab(Task4(), "Задание 4")
        tabs.addTab(Task5(), "Задание 5")
        tabs.addTab(Task6(), "Задание 6")
        
        self.setCentralWidget(tabs)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec()) # Запуск цикла событий приложения