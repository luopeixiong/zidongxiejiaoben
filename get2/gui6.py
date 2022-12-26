from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Example")
        self.layout = QVBoxLayout()
        self.addbnt = QPushButton("Add Button")
        self.removebnt = QPushButton("Remove Button")
        self.printbnt = QPushButton("Print")

        self.addbnt.clicked.connect(self.add_button)
        self.removebnt.clicked.connect(self.remove_button)
        self.printbnt.clicked.connect(self.print_button)


        self.layout.addWidget(self.addbnt)
        self.layout.addWidget(self.removebnt)
        self.layout.addWidget(self.printbnt)
        self.setLayout(self.layout)
        self.buttons = []

    def add_button(self):
        btn1 = QPushButton("Button 1")
        btn2 = QPushButton("Button 2")
        self.layout.addWidget(btn1)
        self.layout.addWidget(btn2)
        self.buttons.append((btn1, btn2))

    def remove_button(self):
        if self.buttons:
            btn1, btn2 = self.buttons.pop()
            btn1.deleteLater()
            btn2.deleteLater()

    def print_button(self):
        print(self.buttons)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
