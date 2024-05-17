import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLCDNumber
from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt


class Program(QWidget):
    def __init__(self):
        super().__init__()
        self._result = False
        self._symbol = False
        self._line = ''
        self.initUI()
        self.show()

    def initUI(self):
        self.setFixedSize(282, 443)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setWindowTitle('Калькулятор')
        self.gridLayout = QWidget(self)
        self.gridLayout.setGeometry(QRect(10, 95, 260, 340))
        self.gridLayout.setObjectName('gridLayout')
        self.grid = QGridLayout(self.gridLayout)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setObjectName('grid')

        self.display = QLCDNumber(self)
        self.display.setGeometry(10, 10, 260, 75)

        positions = [(i, j, 1, 1) for i in range(5) for j in range(4)]
        titles = ['1', '2', '3', '+',
                  '4', '5', '6', '-',
                  '7', '8', '9', '*',
                  '0', '!', '/', '→',
                  '^', '√', 'C', '']
        for position, name in zip(positions, titles):
            if name == '':
                continue
            button = QPushButton(self.gridLayout)
            size = 60
            button.setMaximumSize(size, size)
            button.setMinimumSize(size, size)
            if name == '→':
                button.setMinimumSize(size, size * 2 + 13)
            self.grid.addWidget(button, *position)
            button.setText(name)
            button.clicked.connect(self.actionButton)

    def actionButton(self):
        send = str(self.sender().text())
        value = str(self.display.value())
        if send.isdigit():
            if self._result:
                value = '0.0'
                self._line = ''
                self._result = False
            if self._symbol:
                self._symbol = False
            if value == '0.0':
                value = send 
            elif value[-1] == '0' and value[-2] == '.':
                value = value[:-2] + send
            else:
                value += send
            self._line += send
            self.display.display(float(value))
        elif send in ['+', '-', '*', '/', '^']:
            if not self._symbol:
                if self._result:
                    self._result = False
                if send == '^':
                    self._line += '**'
                else:
                    self._line += send
            self._symbol = True
            self.display.display(0)
        elif send in ['C']:
            self.display.display(0)



        elif send in ['→', '√', '!']:
            try:
                self._line = str(round(eval(self._line), 2))
                if len(self._line) >= 3 and self._line[-1] == '0' and self._line[-2] == '.':
                    self._line = self._line[:-2]
                if send == '√':
                    self._line += '**0.5'
                    self._line = str(round(eval(self._line), 2))
                    if self._line[-1] == '0' and self._line[-2] == '.':
                        self._line = self._line[:-2]
                elif send == '!':
                    if self._line == '0':
                        self._line = '1'
                    else:
                        num = 1
                        for i in range(1, round(eval(self._line)) + 1):
                            num *= i
                        self._line = str(num)
                short = self._line
                if len(self._line) > 5:
                    short = (self._line[0] if self._line[0] != '-' else self._line[:2]) + 'E' + str(len(self._line) - 5)
                self.display.display(short)
                self._symbol = False
                self._result = True
            except:
                self.display.display('Error')


if __name__ == '__main__':
    program = QApplication(sys.argv)
    widget = Program()
    sys.exit(program.exec())
