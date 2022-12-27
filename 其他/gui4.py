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
        self.input_field = None
        self.button = None

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

        self.setLayout(layout)

    def selection_changed(self, index: int) -> None:
        if index == 1:
            # If the input field doesn't exist, create it and add it to the window.
            if not self.input_field:
                self.input_field = QLineEdit()
                self.layout().addRow(self.input_field)
        elif index == 2:
            # If the button doesn't exist, create it and add it to the window.
            if not self.button:
                self.button = QPushButton("Click me!")
                self.layout().addRow(self.button)
        else:
            # If the input field or button exists, remove it from the window.
            if self.input_field:
                self.layout().removeWidget(self.input_field)
                self.input_field.deleteLater()
                self.input_field = None
            if self.button:
                self.layout().removeWidget(self.button)
                self.button.deleteLater()
                self.button = None


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
