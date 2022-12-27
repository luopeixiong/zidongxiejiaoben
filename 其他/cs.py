from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        createButton = QPushButton('Create', self)
        createButton.clicked.connect(self.showMessage)

    def showMessage(self):
        buttonReply = QMessageBox.question(self, 'Confirm', "Are you sure you want to create?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Creating...')
        else:
            print('Cancelled')


if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
