from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFormLayout,
)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the input field, button, and combo box.
        self.input_field = QLineEdit()
        self.input_field.setVisible(False)

        self.button = QPushButton("Click me!")
        self.button.setVisible(False)

        self.combo_box = QComboBox()
        self.combo_box.addItem("0")
        self.combo_box.addItem("1")
        self.combo_box.addItem("2")

        # Connect the combo box's `currentIndexChanged` signal to the
        # `selection_changed` slot.
        self.combo_box.currentIndexChanged.connect(self.selection_changed)

        # Set up the layout.
        layout = QFormLayout()
        layout.addRow("Combo box:", self.combo_box)
        layout.addRow("Input field:", self.input_field)
        layout.addRow("Button:", self.button)

        self.setLayout(layout)

    def selection_changed(self, index: int) -> None:
        if index == 1:
            self.input_field.setVisible(True)
            self.button.setVisible(False)
        elif index == 2:
            self.input_field.setVisible(False)
            self.button.setVisible(True)
        else:
            self.input_field.setVisible(False)
            self.button.setVisible(False)


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
