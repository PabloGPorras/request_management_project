from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,QLineEdit,QComboBox

class CreateRequestWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Create Request Page")
        self.layout.addWidget(self.label)

        # Example form components
        self.input_field1 = QLineEdit()
        self.layout.addWidget(self.input_field1)

        self.input_field2 = QComboBox()
        self.input_field2.addItems(["Option 1", "Option 2", "Option 3"])
        self.layout.addWidget(self.input_field2)

        self.save_button = QPushButton("Save")
        self.layout.addWidget(self.save_button)