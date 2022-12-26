import sys

from PyQt5.QtWidgets import QApplication, QComboBox, QFormLayout, QLineEdit, QPushButton, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

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
        """
        A slot called when the selected index in the combo box changes.

        :param index: The new index of the combo box.
        """
        if index == 0:
            # When the selected index is 0, hide both the input field and
            # the button.
            self.input_field.setVisible(False)
            self.button.setVisible(False)
        elif index == 1:
            # When the selected index is 1, hide the button and show the
            # input field.
            self.input_field.setVisible(True)
            self.button.setVisible(False)
        elif index == 2:
            # When the selected index is 2, hide the input field and show
            # the button.
            self.input_field.setVisible(False)
            self.button.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    # Simulate the user selecting index 0 in the combo box. This will
    # hide both the input field and the button.
    widget.combo_box.setCurrentIndex(0)

    sys.exit(app.exec_())
