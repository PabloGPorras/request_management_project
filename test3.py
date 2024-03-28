from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.button_add = QPushButton("Add Widget")
        self.button_add.clicked.connect(self.add_widget)
        self.layout.addWidget(self.button_add)

        self.button_remove = QPushButton("Remove Widget")
        self.button_remove.clicked.connect(self.remove_widget)
        self.layout.addWidget(self.button_remove)

        label = QLabel("New Widget")
        self.stacked_widget.addWidget(label)

    def add_widget(self):
        current_index = self.stacked_widget.currentIndex()
        current_widget = self.stacked_widget.widget(current_index)

        label = QLabel("New Widget")
        current_widget.layout().addWidget(label)
        print("Widget added to current stacked widget's layout.")


    def remove_widget(self):
        if self.stacked_widget.count() > 0:
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
            print("Widget removed. Total widgets:", self.stacked_widget.count())

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
