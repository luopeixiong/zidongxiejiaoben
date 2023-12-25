from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLineEdit, QPushButton, QSpinBox, QToolButton, QVBoxLayout, QWidget


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        widget1 = QPushButton("widget1")
        widget2 = QSpinBox()
        widget3 = QComboBox()
        widget4 = QLineEdit()

        bottomWidget = QToolButton(text="botton")
        # first create the four widgets at the top left,
        # and use QWidget::setFixedWidth() on each of them.

        # then set up the top widget (composed of the four smaller widgets):

        topWidget = QWidget()
        topWidgetLayout = QHBoxLayout(topWidget)
        topWidgetLayout.addWidget(widget1)
        topWidgetLayout.addWidget(widget2)
        topWidgetLayout.addWidget(widget3)
        topWidgetLayout.addWidget(widget4)
        topWidgetLayout.addStretch(1)
        topWidget.setFixedHeight(50)

        # now put the bottom (centered) widget into its own QHBoxLayout
        hLayout = QHBoxLayout()
        hLayout.addStretch(1)
        hLayout.addWidget(bottomWidget)
        hLayout.addStretch(1)
        bottomWidget.setFixedSize(QSize(50, 50))

        # now use a QVBoxLayout to lay everything out
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(topWidget)
        mainLayout.addStretch(1)
        mainLayout.addLayout(hLayout)
        mainLayout.addStretch(1)

        self.setLayout(mainLayout)
        self.resize(640, 480)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = Widget()
    w.show()
    sys.exit(app.exec_())