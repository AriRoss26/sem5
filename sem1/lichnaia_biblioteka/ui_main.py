from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Виджет 1: Лейбл
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lbl_title.setFont(font)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setObjectName("lbl_title")
        self.verticalLayout.addWidget(self.lbl_title)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Виджет 2: Таблица
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget)
        
        # Правая панель для обложки и кнопок
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.lbl_cover = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cover.setMinimumSize(QtCore.QSize(200, 300))
        self.lbl_cover.setMaximumSize(QtCore.QSize(200, 300))
        self.lbl_cover.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_cover.setScaledContents(True)
        self.lbl_cover.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_cover.setObjectName("lbl_cover")
        self.verticalLayout_2.addWidget(self.lbl_cover)
        
        # Виджет 3: Кнопка
        self.btn_add = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add.setObjectName("btn_add")
        self.verticalLayout_2.addWidget(self.btn_add)
        
        self.btn_edit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_edit.setObjectName("btn_edit")
        self.verticalLayout_2.addWidget(self.btn_edit)
        
        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setObjectName("btn_delete")
        self.verticalLayout_2.addWidget(self.btn_delete)
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Личная библиотека"))
        self.lbl_title.setText(_translate("MainWindow", "Моя Библиотека"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Название"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Автор"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Год"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Жанр"))
        self.lbl_cover.setText(_translate("MainWindow", "Обложка"))
        self.btn_add.setText(_translate("MainWindow", "Добавить"))
        self.btn_edit.setText(_translate("MainWindow", "Редактировать"))
        self.btn_delete.setText(_translate("MainWindow", "Удалить (или Delete)"))