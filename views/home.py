from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.refresh_button = QPushButton("Refresh")
        self.layout.addWidget(self.refresh_button)

        self.request_table = QTableWidget()
        self.request_table.setColumnCount(3)  # Example: Change the number of columns as needed
        self.request_table.setHorizontalHeaderLabels(["ID", "Type", "Date"])  # Example: Change column headers as needed
        self.layout.addWidget(self.request_table)

        self.filter_button = QPushButton("Filter")
        self.layout.addWidget(self.filter_button)
