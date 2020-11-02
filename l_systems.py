import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor
from math import cos, sin, radians, pi
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5 import QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(566, 508)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 459, QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.slider = QtWidgets.QSlider(Form)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMaximum(20)
        self.slider.setObjectName("slider")
        self.verticalLayout.addWidget(self.slider)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "L - системы"))


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.do_paint = False
        self.slider.sliderMoved.connect(self.paint)

        try:
            filename = QFileDialog.getOpenFileName(self, 'Выбрать файл с описанием L-системы', '',
                                                   'l_system_description (*.ls);;Все файлы (*)')[0]
            with open(filename, 'r', encoding='utf-8') as f:
                data = [x.strip() for x in f.read().split('\n') if x]
            title, self.n, self.axiom, *data = data
            self.n = int(self.n)
            self.setWindowTitle(str(title))
            self.d = {}
            for line in data:
                key, value = line.split()
                self.d[key] = value
        except Exception as e:
            sys.exit()

    def paint(self):
        self.do_paint = True
        self.repaint()
        self.do_paint = False

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_flag(qp)
            qp.end()

    def draw_flag(self, qp):
        qp.setBrush(QColor(0, 0, 0))

        temp_string = self.axiom
        steps = int(self.slider.value())

        for i in range(steps):
            temp_string = ''.join([self.d.get(x, x) for x in temp_string])

        stack = []
        cords = (int(self.width() // 2),
                 int(self.height() // 2))
        angle = 0
        length = 5

        for symbol in temp_string:
            if symbol == 'F':
                new_cords = (int(length * cos(radians(360 / self.n) * angle) + cords[0]),
                             int(length * sin(radians(360 / self.n) * angle) + cords[1]))
                qp.drawLine(*cords, *new_cords)
                cords = new_cords[:]
            elif symbol == '+':
                angle = (angle + 1) % self.n
            elif symbol == '-':
                angle = (angle - 1) % self.n
            elif symbol == '[':
                stack.append((cords, angle))
            elif symbol == ']':
                cords, angle = stack.pop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
