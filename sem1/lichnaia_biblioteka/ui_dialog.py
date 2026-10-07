from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BookDialog(object):
    def setupUi(self, BookDialog):
        BookDialog.setObjectName("BookDialog")
        BookDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(BookDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        
        self.label = QtWidgets.QLabel(BookDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        
        # Виджет 4: LineEdit
        self.le_title = QtWidgets.QLineEdit(BookDialog)
        self.le_title.setObjectName("le_title")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_title)
        
        self.label_2 = QtWidgets.QLabel(BookDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        
        self.le_author = QtWidgets.QLineEdit(BookDialog)
        self.le_author.setObjectName("le_author")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_author)
        
        self.label_3 = QtWidgets.QLabel(BookDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        
        self.le_year = QtWidgets.QLineEdit(BookDialog)
        self.le_year.setObjectName("le_year")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.le_year)
        
        self.label_4 = QtWidgets.QLabel(BookDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        
        # Виджет 5: ComboBox
        self.cb_genre = QtWidgets.QComboBox(BookDialog)
        self.cb_genre.setObjectName("cb_genre")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cb_genre)
        self.verticalLayout.addLayout(self.formLayout)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_cover_path = QtWidgets.QLineEdit(BookDialog)
        self.le_cover_path.setReadOnly(True)
        self.le_cover_path.setObjectName("le_cover_path")
        self.horizontalLayout.addWidget(self.le_cover_path)
        
        self.btn_browse = QtWidgets.QPushButton(BookDialog)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.buttonBox = QtWidgets.QDialogButtonBox(BookDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(BookDialog)
        self.buttonBox.accepted.connect(BookDialog.accept)
        self.buttonBox.rejected.connect(BookDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BookDialog)

    def retranslateUi(self, BookDialog):
        _translate = QtCore.QCoreApplication.translate
        BookDialog.setWindowTitle(_translate("BookDialog", "Данные о книге"))
        self.label.setText(_translate("BookDialog", "Название:"))
        self.label_2.setText(_translate("BookDialog", "Автор:"))
        self.label_3.setText(_translate("BookDialog", "Год издания:"))
        self.label_4.setText(_translate("BookDialog", "Жанр:"))
        self.btn_browse.setText(_translate("BookDialog", "Обложка..."))