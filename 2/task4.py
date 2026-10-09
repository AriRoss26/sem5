import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic

class NimGame(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('task4.ui', self)
        
        self.btn_start.clicked.connect(self.start_game)
        self.btn_take.clicked.connect(self.player_turn)
        self.stones = 0

    def start_game(self):
        self.stones = self.start_stones_spin.value()
        self.update_ui()
        self.take_spin.setEnabled(True)
        self.btn_take.setEnabled(True)
        self.lbl_log.setText("Ваш ход! Вы берете первыми.")

    def update_ui(self):
        self.lbl_remaining.setText(f"Камней осталось: {self.stones}")
        self.take_spin.setMaximum(min(3, self.stones) if self.stones > 0 else 3)

    def player_turn(self):
        take = self.take_spin.value()
        self.stones -= take
        self.update_ui()
        
        if self.stones == 0:
            self.game_over("Вы победили!")
            return

        self.lbl_log.setText(f"Вы взяли {take}. Ход компьютера...")
        self.computer_turn()

    def computer_turn(self):
        # Алгоритм ИИ: всегда стараться оставлять противнику число камней кратное 4
        remainder = self.stones % 4
        take = remainder if remainder != 0 else 1
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
        QMessageBox.information(self, "Конец", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NimGame()
    ex.show()
    sys.exit(app.exec_())