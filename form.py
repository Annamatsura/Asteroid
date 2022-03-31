import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_form(object):
    """
    Класс с формой меню
    """

    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(429, 730)
        form.setStyleSheet("#form{border-image:url(fon.jpg)}")
        self.pushButton = QtWidgets.QPushButton(form)
        self.pushButton.setGeometry(QtCore.QRect(140, 660, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start_game)

        self.spinBox = QtWidgets.QSpinBox(form)
        self.spinBox.setGeometry(QtCore.QRect(170, 100, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(15)
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(form)
        self.spinBox_2.setGeometry(QtCore.QRect(170, 600, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(5)
        self.spinBox_2.setObjectName("spinBox_2")
        self.lineEdit = QtWidgets.QLineEdit(form)
        self.lineEdit.setGeometry(QtCore.QRect(130, 50, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(form)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 550, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.spinBox_3 = QtWidgets.QSpinBox(form)
        self.spinBox_3.setGeometry(QtCore.QRect(110, 190, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_3.setFont(font)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setObjectName("spinBox_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(form)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 150, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.spinBox_4 = QtWidgets.QSpinBox(form)
        self.spinBox_4.setGeometry(QtCore.QRect(230, 190, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_4.setFont(font)
        self.spinBox_4.setMinimum(2)
        self.spinBox_4.setMaximum(7)
        self.spinBox_4.setObjectName("spinBox_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(form)
        self.lineEdit_4.setGeometry(QtCore.QRect(130, 390, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.spinBox_5 = QtWidgets.QSpinBox(form)
        self.spinBox_5.setGeometry(QtCore.QRect(130, 430, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_5.setFont(font)
        self.spinBox_5.setMinimum(640)
        self.spinBox_5.setMaximum(1500)
        self.spinBox_5.setValue(1024)
        self.spinBox_5.setObjectName("spinBox_5")
        self.spinBox_6 = QtWidgets.QSpinBox(form)
        self.spinBox_6.setGeometry(QtCore.QRect(220, 430, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_6.setFont(font)
        self.spinBox_6.setMinimum(480)
        self.spinBox_6.setMaximum(1200)
        self.spinBox_6.setValue(768)
        self.spinBox_6.setObjectName("spinBox_6")
        self.line = QtWidgets.QFrame(form)
        self.line.setGeometry(QtCore.QRect(0, 330, 421, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lineEdit_5 = QtWidgets.QLineEdit(form)
        self.lineEdit_5.setGeometry(QtCore.QRect(80, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(form)
        self.lineEdit_6.setGeometry(QtCore.QRect(100, 240, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.spinBox_7 = QtWidgets.QSpinBox(form)
        self.spinBox_7.setGeometry(QtCore.QRect(100, 280, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_7.setFont(font)
        self.spinBox_7.setMinimum(3)
        self.spinBox_7.setValue(20)
        self.spinBox_7.setObjectName("spinBox_7")
        self.spinBox_8 = QtWidgets.QSpinBox(form)
        self.spinBox_8.setGeometry(QtCore.QRect(240, 280, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox_8.setFont(font)
        self.spinBox_8.setMinimum(20)
        self.spinBox_8.setValue(50)
        self.spinBox_8.setMaximum(120)
        self.spinBox_8.setObjectName("spinBox_8")
        self.lineEdit_7 = QtWidgets.QLineEdit(form)
        self.lineEdit_7.setGeometry(QtCore.QRect(100, 350, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.line_2 = QtWidgets.QFrame(form)
        self.line_2.setGeometry(QtCore.QRect(0, 490, 421, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.lineEdit_8 = QtWidgets.QLineEdit(form)
        self.lineEdit_8.setGeometry(QtCore.QRect(90, 510, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.line_3 = QtWidgets.QFrame(form)
        self.line_3.setGeometry(QtCore.QRect(0, 640, 421, 21))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.lineEdit_9 = QtWidgets.QLineEdit(form)
        self.lineEdit_9.setGeometry(QtCore.QRect(40, 190, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(form)
        self.lineEdit_10.setGeometry(QtCore.QRect(40, 280, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(form)
        self.lineEdit_11.setGeometry(QtCore.QRect(330, 190, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(form)
        self.lineEdit_12.setGeometry(QtCore.QRect(340, 280, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setObjectName("lineEdit_12")

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Menu"))
        self.pushButton.setText(_translate("form", "Start game"))
        self.lineEdit.setText(_translate("form", "Кол-во шаров"))
        self.lineEdit_2.setText(_translate("form", "Кол-во жизней"))
        self.lineEdit_3.setText(_translate("form", "Границы скорости"))
        self.lineEdit_4.setText(_translate("form", "Размеры поля"))
        self.lineEdit_5.setText(_translate("form", "Настройка шаров"))
        self.lineEdit_6.setText(_translate("form", "Границы размеров"))
        self.lineEdit_7.setText(_translate("form", "Настройка поля"))
        self.lineEdit_8.setText(_translate("form", "Настройка игрока"))
        self.lineEdit_9.setText(_translate("form", "min"))
        self.lineEdit_10.setText(_translate("form", "min"))
        self.lineEdit_11.setText(_translate("form", "max"))
        self.lineEdit_12.setText(_translate("form", "max"))

    def get_info(self):
        """
        Получчает информацию с формы
        :return: список с информацией
        """
        numb_balls = self.spinBox.value()
        min_speed = self.spinBox_3.value()
        max_speed = self.spinBox_4.value()
        min_radius = self.spinBox_7.value()
        max_radius = self.spinBox_8.value()
        min_field = self.spinBox_5.value()
        max_field = self.spinBox_6.value()
        lives = self.spinBox_2.value()
        list_info = [numb_balls, min_speed, max_speed, min_radius,
                     max_radius, min_field, max_field, lives]

        return list_info

    def write_info(self, lines):
        """
        записывает информацию в файл построчно
        :param lines: список с информацией
        :return: None
        """
        for i in lines:
            print('** ', i)
        with open("test.txt", "w") as file:
            for line in lines:
                file.write(str(line) + '\n')

    def start_game(self):
        """
        слот для нажатия кнопки start game
        записывает информацию, полученную с формы в файл
        и запускает файл с игрой
        :return: None
        """
        list_info = self.get_info()
        self.write_info(list_info)
        import game_play


if __name__ == "__main__":
    """
    Точка входа в программу
    """

    app = QtWidgets.QApplication(sys.argv)
    window = Ui_form()
    w = QtWidgets.QMainWindow()
    window.setupUi(w)
    w.show()
    sys.exit(app.exec_())

