from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QScrollArea
import json

from sqlalchemy import Column, inspect
from models.model import Model
from database.engine import getEngine, getSession
from models.modelBuilder import ModelBuilder

class ColumnWidget(QWidget):
    def __init__(self, remove_callback):
        super().__init__()

        self.remove_callback = remove_callback

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.column_name_label = QLabel("Column Name:")
        self.layout.addWidget(self.column_name_label)
        self.column_name_input = QLineEdit()
        self.layout.addWidget(self.column_name_input)

        self.column_type_label = QLabel("Column Type:")
        self.layout.addWidget(self.column_type_label)
        self.column_type_input = QComboBox()
        self.column_type_input.addItems(["string", "integer"])
        self.layout.addWidget(self.column_type_input)

        self.column_length_label = QLabel("Column Length:")
        self.layout.addWidget(self.column_length_label)
        self.column_length_input = QLineEdit()
        self.layout.addWidget(self.column_length_input)

        self.default_value_label = QLabel("Default Value:")
        self.layout.addWidget(self.default_value_label)
        self.default_value_input = QLineEdit()
        self.layout.addWidget(self.default_value_input)

        self.primary_key_label = QLabel("Primary Key:")
        self.layout.addWidget(self.primary_key_label)
        self.primary_key_input = QComboBox()
        self.primary_key_input.addItems(["True", "False"])
        self.layout.addWidget(self.primary_key_input)

        self.include_in_user_form_label = QLabel("Include in User Form:")
        self.layout.addWidget(self.include_in_user_form_label)
        self.include_in_user_form_input = QComboBox()
        self.include_in_user_form_input.addItems(["True", "False"])
        self.layout.addWidget(self.include_in_user_form_input)

        self.include_in_worker_form_label = QLabel("Include in Worker Form:")
        self.layout.addWidget(self.include_in_worker_form_label)
        self.include_in_worker_form_input = QComboBox()
        self.include_in_worker_form_input.addItems(["True", "False"])
        self.layout.addWidget(self.include_in_worker_form_input)

        self.validates_label = QLabel("Validates:")
        self.layout.addWidget(self.validates_label)
        self.validates_input = QLineEdit()
        self.layout.addWidget(self.validates_input)

        self.column_options_label = QLabel("Dropdown Options (if any):")
        self.layout.addWidget(self.column_options_label)
        self.column_options_input = QLineEdit()
        self.layout.addWidget(self.column_options_input)

        self.remove_button = QPushButton("Remove Column")
        self.remove_button.clicked.connect(self.remove_callback)
        self.layout.addWidget(self.remove_button)


class ModelEditorScreen(QWidget):
    def __init__(self, parent=None, props={}, *args, **kwargs):
        super(ModelEditorScreen, self).__init__(parent)
        self.parent = parent
        self.props = props

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Table Name Input
        self.table_name_label = QLabel("Table Name:")
        self.layout.addWidget(self.table_name_label)
        self.table_name_input = QLineEdit()
        self.layout.addWidget(self.table_name_input)

        # Table Args Input
        self.table_args_label = QLabel("Table Args:")
        self.layout.addWidget(self.table_args_label)
        self.table_args_input = QLineEdit()  # You can replace this with appropriate widget based on your requirements
        self.layout.addWidget(self.table_args_input)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.layout.addWidget(self.scroll_area)

        self.columns = []

        self.add_column_button = QPushButton("Add Column")
        self.add_column_button.clicked.connect(self.add_column)
        self.layout.addWidget(self.add_column_button)

        self.generate_button = QPushButton("Generate JSON")
        self.generate_button.clicked.connect(self.generate_json)
        self.layout.addWidget(self.generate_button)

        if "model" in self.props:
            self.load_model(self.props["model"])

    def load_model(self, model):
        self.table_name_input.setText(model.model_name)
        model_data = json.loads(model.model_json)
        self.table_args_input.setText("")  # Clear table args input
        for column_data in model_data["table_columns"]:
            column_widget = ColumnWidget(self.remove_column)
            column_widget.column_name_input.setText(column_data["name"])
            column_widget.column_type_input.setCurrentText(column_data["type"])
            column_widget.column_length_input.setText(str(column_data.get("length", "")))
            column_widget.default_value_input.setText(column_data.get("default", ""))
            column_widget.primary_key_input.setCurrentText("True" if column_data.get("primary_key", False) else "False")
            column_widget.include_in_user_form_input.setCurrentText("True" if column_data.get("include_in_user_form", False) else "False")
            column_widget.include_in_worker_form_input.setCurrentText("True" if column_data.get("include_in_worker_form", False) else "False")
            column_widget.validates_input.setText(json.dumps(column_data.get("validates", {})))
            column_widget.column_options_input.setText(", ".join(column_data.get("options", [])))
            self.columns.append(column_widget)
            self.scroll_layout.addWidget(column_widget)
            self.scroll_layout.addSpacing(30)  # Add spacing between columns

    def add_column(self):
        column_widget = ColumnWidget(self.remove_column)
        self.columns.append(column_widget)
        self.scroll_layout.addWidget(column_widget)
        self.scroll_layout.addSpacing(30)  # Add spacing between columns

    def remove_column(self):
        sender_button = self.sender()  # Get the button that triggered the signal
        column_widget = sender_button.parent()  # Get the parent widget (ColumnWidget)
        if column_widget in self.columns:
            self.scroll_layout.removeWidget(column_widget)
            column_widget.deleteLater()  # Delete the widget from memory
            self.columns.remove(column_widget)

    def generate_json(self):
        data = {
            "table_name": self.table_name_input.text(),
            "table_args": {},  # You may need to process this input accordingly
            "table_columns": []
        }

        for column_widget in self.columns:
            column_data = {
                "name": column_widget.column_name_input.text(),
                "type": column_widget.column_type_input.currentText(),  # Use currentText to get selected item
                "length": int(column_widget.column_length_input.text()) if column_widget.column_length_input.text() and column_widget.column_length_input.text() != 'None' else None,
                "primary_key": column_widget.primary_key_input.currentText() == "True",
                "default": column_widget.default_value_input.text(),
                "validates": json.loads(column_widget.validates_input.text()) if column_widget.validates_input.text() else {},
                "include_in_user_form": column_widget.include_in_user_form_input.currentText() == "True",
                "include_in_worker_form": column_widget.include_in_worker_form_input.currentText() == "True"
            }
            options_text = column_widget.column_options_input.text().strip()  # Remove leading and trailing spaces
            if options_text:
                column_data["options"] = [option.strip() for option in options_text.split(",")]
            data["table_columns"].append(column_data)

        json_data = json.dumps(data, indent=4)
        print(json_data)

        model_builder = ModelBuilder()
        with getSession() as session:
            if "model" in self.props:
                # Update existing model
                model = self.props["model"]
                model.model_json = json_data
                table = model_builder.createModel(model)

                # Commit the changes to the database
                table.metadata.create_all(getEngine())
            else:
                # Create new model
                model = Model(model_name=data["table_name"], model_json=json_data)
                session.add(model)
                session.commit()
                # Create the corresponding table
                table = model_builder.createModel(model)

        return table