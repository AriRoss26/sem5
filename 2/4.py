import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QSpinBox, QPushButton, QLabel, QMessageBox)

class NimGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Игра «Псевдоним»')
        self.resize(300, 200)
        layout = QVBoxLayout()
        # Настройка игры
        setup_layout = QHBoxLayout()
        setup_layout.addWidget(QLabel("Начальное кол-во камней:"))
        self.start_stones_spin = QSpinBox()
        self.start_stones_spin.setRange(5, 100)
        self.start_stones_spin.setValue(20)
        setup_layout.addWidget(self.start_stones_spin)
        self.btn_start = QPushButton("Начать новую игру")
        self.btn_start.clicked.connect(self.start_game)
        layout.addLayout(setup_layout)
        layout.addWidget(self.btn_start)
        # Игровой процесс
        self.lbl_remaining = QLabel("Камней осталось: -")
        font = self.lbl_remaining.font()
        font.setPointSize(14)
        self.lbl_remaining.setFont(font)
        layout.addWidget(self.lbl_remaining)
        play_layout = QHBoxLayout()
        play_layout.addWidget(QLabel("Взять камней (1-3):"))
        self.take_spin = QSpinBox()
        self.take_spin.setRange(1, 3)
        self.take_spin.setEnabled(False)
        play_layout.addWidget(self.take_spin)
        self.btn_take = QPushButton("Взять")
        self.btn_take.setEnabled(False)
        self.btn_take.clicked.connect(self.player_turn)
        play_layout.addWidget(self.btn_take)
        layout.addLayout(play_layout)
        self.lbl_log = QLabel("Нажмите 'Начать новую игру'")
        layout.addWidget(self.lbl_log)
        self.setLayout(layout)
        self.stones = 0
    def start_game(self):
        self.stones = self.start_stones_spin.value()
        self.update_ui()
        self.take_spin.setEnabled(True)
        self.btn_take.setEnabled(True)
        self.lbl_log.setText("Ваш ход! Вы берете первыми.")
    def update_ui(self):
        self.lbl_remaining.setText(f"Камней осталось: {self.stones}")
        # Ограничиваем ввод, если камней осталось меньше 3
        self.take_spin.setMaximum(min(3, self.stones) if self.stones > 0 else 3)
    def player_turn(self):
        take = self.take_spin.value()
        self.stones -= take
        self.update_ui()
        if self.stones == 0:
            self.game_over("Вы победили!")
            return
        self.lbl_log.setText(f"Вы взяли {take}. Ход компьютера...")
        # Небольшая задержка для визуализации
        self.computer_turn()
    def computer_turn(self):
        # Идеальная стратегия ИИ: оставлять кратное 4
        remainder = self.stones % 4
        if remainder == 0:
            # Позиция проигрышная для ИИ: берем 1 камень наугад, чтобы затянуть игру
            take = 1
        else:
            # Забираем остаток, чтобы оставить игроку число кратное 4
            take = remainder
        take = min(take, self.stones)
        self.stones -= take
        self.update_ui()
        self.lbl_log.setText(f"Компьютер взял {take}. Ваш ход.")
        if self.stones == 0:
            self.game_over("Компьютер победил!")
    def game_over(self, message):
        self.take_spin.setEnabled(False)
        self.btn_take.setEnabled(False)
        self.lbl_log.setText(message)
        QMessageBox.information(self, "Конец игры", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NimGame()
    ex.show()
    sys.exit(app.exec_())