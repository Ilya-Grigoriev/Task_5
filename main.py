import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QStackedWidget, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.upload.clicked.connect(self.open_table)
        self.tools.clicked.connect(self.move_tab)

    def open_table(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM date", ).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'name_variety', 'degree', 'type', 'description', 'price', 'size'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def move_tab(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.resize(289, 361)


class Tools(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.create.clicked.connect(self.func_create)
        self.edit.clicked.connect(self.func_edit)
        self.revert.clicked.connect(self.func_exit)

    def func_create(self):
        self.statusBar().showMessage('')
        name, degree, type_coffee = self.name.text().strip(), self.degree.text().strip(), self.type.text().strip()
        desc, price, size = self.desc.toPlainText().strip(), self.price.value(), self.size.value()
        if not (name and degree and type_coffee and desc and price and size) or type_coffee.lower() not in (
                'молотый', 'в зёрнах', 'в зернах'):
            self.statusBar().showMessage('Введены некорректные данные')
        else:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            len_date = len(list(cur.execute("""SELECT * FROM date""").fetchall()))
            cur.execute(
                "INSERT INTO date (id, name_variety, degree, type, description, price, size) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (len_date + 1, name, degree, type_coffee, desc, price, size)).fetchall()
            con.commit()
            con.close()

    def func_edit(self):
        self.statusBar().showMessage('')
        try:
            row, col = int(self.row.value()), int(self.col.value())
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            len_date = len(list(cur.execute("SELECT * FROM date")))
            if row > len_date or not self.date_val.text().strip():
                raise Exception
            columns = ['id', 'name_variety', 'degree', 'type', 'description', 'price', 'size'][col]
            if col > 4:
                cur_date = float(self.date_val.text())
            else:
                cur_date = f'"{self.date_val.text()}"'
            request = f"UPDATE date SET {columns} = {cur_date} WHERE id={row}"
            cur.execute(request).fetchall()
            con.commit()
            con.close()
        except Exception:
            self.statusBar().showMessage('Введены некорректные данные')

    def func_exit(self):
        self.statusBar().showMessage('')
        self.name.clear()
        self.degree.clear()
        self.type.clear()
        self.desc.clear()
        self.price.setValue(0.00)
        self.size.setValue(0.00)
        self.row.setValue(0)
        self.col.setValue(0)
        self.date_val.clear()
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.resize(380, 392)


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    widget.addWidget(MyWidget())
    widget.addWidget(Tools())
    widget.resize(380, 392)
    widget.move(300, 50)
    widget.show()
    sys.exit(app.exec())
