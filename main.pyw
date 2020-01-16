import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidget

import mainwindow_ui  # Это наш конвертированный файл дизайна
import sportsmen
import add_change_sportsmen


class AddSportsmen(QtWidgets.QDialog, add_change_sportsmen.Ui_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Добавление/редактирование")
        self.pushButton.clicked.connect(self.__add_sportsmen)
        self.pushButton_2.clicked.connect(self.__edit_sportsmen)

    def __full(self):
        temp_1 = self.lineEdit_3.text();
        temp_2 = self.lineEdit_4.text()
        if (self.lineEdit.text() == "" or self.lineEdit_2.text() == "" or self.lineEdit_3.text() == ""
                or self.lineEdit_4.text() == ""):
            return 1
        else:
            return 0

    def __clean(self):  # очищение полей после добавления
        self.lineEdit.clear();
        self.lineEdit_2.clear();
        self.lineEdit_3.clear();
        self.lineEdit_4.clear();

    ##    def is_number(s):
    ##        try:
    ##            float(s)
    ##            return True
    ##        except ValueError:
    ##            return False

    def __add_sportsmen(self):
        if (self.__full() == 0):
            if (os.path.exists("course.txt")):  # существование файла
                f = open("course.txt", "r")
                lines = f.readlines()
                if not lines:
                    amount = 0
                else:
                    amount = int(lines[0])
                f.close()

                f = open("course.txt", "w")
                f.write(str(amount + 1) + "\n")
                for i in range(1, len(lines)):
                    f.write(lines[i])
                f.write(self.lineEdit.text() + "," + self.lineEdit_2.text() + "," + self.lineEdit_3.text() + "," +
                        self.lineEdit_4.text() + "\n")
                f.close()
                msg = QMessageBox.information(self, "Информация", "Успешно добавлен!")
                self.__clean()  # очистка
                del lines
        else:
            msg = QMessageBox.warning(self, "Ошибка", "Проверьте заполненность всех полей")

    def full_for_Edit(self):
        f = open("course.txt", "r")
        lines = f.readlines()
        f.close()
        split_mas = lines[self.number + 1].split(",")

        self.lineEdit.setText(str(split_mas[0]));
        self.lineEdit_2.setText(split_mas[1]);
        self.lineEdit_3.setText(split_mas[2])
        self.lineEdit_4.setText(split_mas[3].replace("\n", ""))
        del lines, split_mas

    def __edit_sportsmen(self):
        if (self.__full() == 0):
            f = open("course.txt", "r")
            lines = f.readlines()
            f.close()

            split_mas = lines[self.number + 1].split(",")
            split_mas[0] = self.lineEdit.text();
            split_mas[1] = self.lineEdit_2.text();
            split_mas[2] = self.lineEdit_3.text()
            split_mas[3] = self.lineEdit_4.text() + "\n"

            temp = ','.join(split_mas)  # перевод в строку
            lines[self.number + 1] = temp
            f = open("course.txt", "w")
            for i in range(len(lines)):
                f.write(lines[i])
            f.close()

            msg = QMessageBox.information(self, "Информация", "Отредактировано!")
            del lines, split_mas
        else:
            msg = QMessageBox.warning(self, "Ошибка", "Проверьте заполненность всех полей")


""" _______________________________________________________________________________________________"""
""" _______________________________________________________________________________________________"""
""" _______________________________________________________________________________________________"""


class MainWindow(QtWidgets.QMainWindow, mainwindow_ui.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowTitle("БД Спортсмены")
        if not os.path.exists("course.txt"):
            f = open("course.txt", "w");
            f.write(str(0));
            f.close()
        self.pushButton.clicked.connect(self.__open_dialog)
        self.pushButton_2.clicked.connect(self.__delete_sportsmen)
        self.pushButton_3.clicked.connect(self.__edit_sportsmen)
        self.pushButton_4.clicked.connect(self.__winners_sportsmen)
        self.pushButton_5.clicked.connect(self.__speed_sportsmen)
        self.filling()  # заполнение listWidget

    def __open_dialog(self):
        window = AddSportsmen()
        window.pushButton_2.setVisible(False)
        window.exec_()
        if (window.close()):
            self.listWidget.clear()
            self.filling()

    def __delete_sportsmen(self):

        f = open("course.txt", "r")
        lines = f.readlines()
        f.close()

        if (self.listWidget.currentRow() == -1):
            msg = QMessageBox.warning(self, "Ошибка", "Выберите объект")
            return
        else:
            lines.pop(self.listWidget.currentRow() + 1)

        lines[0] = int(lines[0]);
        lines[0] -= 1;
        lines[0] = str(lines[0]) + "\n"
        f = open("course.txt", "w")
        for i in range(len(lines)):
            f.write(str(lines[i]))
        f.close()

        # удаление из QListWidget
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

        msg = QMessageBox.information(self, "info", "Удалено!")

    def __edit_sportsmen(self):

        if (self.listWidget.currentRow() == -1):
            msg = QMessageBox.warning(self, "Ошибка", "Выберите объект")
            return
        else:
            window = AddSportsmen()
            window.pushButton.setVisible(False)
            window.number = self.listWidget.currentRow()  # передаем значение строки в Dialog Window
            window.full_for_Edit()
            window.exec_()
            if (window.close()):
                self.listWidget.clear()
                self.filling()

    def __winners_sportsmen(self):
        self.listWidget_2.clear()
        A = list()
        f = open("course.txt", "r")
        lines = f.readlines()
        f.close()

        for i in range(1, len(lines)):
            split_mas = lines[i].split(",")
            split_mas[3] = split_mas[3].replace("\n", "")
            B = sportsmen.Sportsmen()
            B.set_Fam(split_mas[0]);
            B.set_Name(split_mas[1])
            B.set_Long(float(split_mas[2]));
            B.set_Short(float(split_mas[3]));
            A.append(B)
            del split_mas

        winner_short, winner_long = A[0].get_Fam(), A[0].get_Fam()
        win_org_short, win_org_long = A[0].get_Name(), A[0].get_Name()
        # минимальное время
        min_time_short = A[0].get_Short()
        min_time_long = A[0].get_Long()
        for i in range(1, len(A)):
            if (min_time_short > A[i].get_Short()):
                winner_short = A[i].get_Fam()
                win_org_short = A[i].get_Name()
                min_time_short = A[i].get_Short()
            if (min_time_long > A[i].get_Long()):
                winner_long = A[i].get_Fam()
                win_org_long = A[i].get_Name()
                min_time_long = A[i].get_Long()
        self.listWidget_2.addItem('Победитель длинной дистанции: ' + winner_long + "\nОрганизация: " + win_org_long +
                                  '\nПобедитель короткой дистанции: ' + winner_short + "\nОрганизация: " + win_org_short)

    def __speed_sportsmen(self):
        self.listWidget_2.clear()
        A = list()
        f = open("course.txt", "r")
        lines = f.readlines()
        f.close()

        for i in range(1, len(lines)):
            split_mas = lines[i].split(",")
            split_mas[3] = split_mas[3].replace("\n", "")
            B = sportsmen.Sportsmen()
            B.set_Fam(split_mas[0]);
            B.set_Name(split_mas[1])
            B.set_Long(float(split_mas[2]));
            B.set_Short(float(split_mas[3]));
            A.append(B)
            del split_mas

        copy_mas = list()
        for i in range(len(A)):
            copy_mas.append(A[i].Name)
        copy_mas = list(set(copy_mas))  # удаление повторяющихся элементов
        av_speed_mas = list()  # массив средних скоростей
        for i in range(len(copy_mas)):
            sum_speed = 0  # суммарная скорость = 0
            amount_speed = 0  # участники одной орг-ии
            for j in range(len(A)):
                if (copy_mas[i] == A[j].get_Name()):  # если наименования совпадают
                    sum_speed += 100 / A[j].get_Short()
                    amount_speed += 1
            av_res = sum_speed / amount_speed
            av_speed_mas.append(av_res)
        win_speed_index = 0  # победитель по скорости
        high_speed = av_speed_mas[0]
        for i in range(len(av_speed_mas) - 1):
            if (high_speed < av_speed_mas[i + 1]):
                win_speed_index = i + 1
                high_speed = av_speed_mas[i + 1]
        self.listWidget_2.addItem("Организация победитель\nпо средней скорости на 100м: " + copy_mas[win_speed_index])
        del av_speed_mas, copy_mas

    def filling(self):
        if (os.path.exists("course.txt")):
            f = open("course.txt", "r")
            lines = f.readlines()
            for i in range(1, len(lines)):
                split_mas = lines[i].split(",")  # создание массива из элементов отделен. пробелами
                self.listWidget.addItem(
                    "Фамилия: " + split_mas[0] + "\nОрганизация: " + split_mas[1] + "\nВремя пробега 1 км(мин.с): "
                    + split_mas[2] + "\nВремя пробега 100 м(с): " + split_mas[3])
            f.close()

        del lines


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
