import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QDialogButtonBox, QFormLayout
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
import json
from PyQt6.QtWidgets import QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dynamic Model App")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.engine = create_engine('sqlite:///dynamic_models.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.model_json = {
    "table_name": "rule_request",
    "table_args": {},
    "table_columns": [
        {
            "name": "request_id",
            "type": "string",
            "length": 20,
            "primary_key": True,
            "default": "",
            "validates": {"presence": True, "length": {"minimum": 1, "maximum": 20}},
            "include_in_form": True
        },
        {
            "name": "request_type",
            "type": "string",
            "length": 50,
            "default": "default_type",
            "validates": {"presence": True, "length": {"minimum": 1, "maximum": 50}},
            "include_in_form": True,
            "options": ["Type A", "Type B", "Type C"]  # Dropdown options for request_type column
        },
        {
            "name": "request_date",
            "type": "string",
            "length": 10,
            "validates": {"presence": True, "format": "date"},
            "include_in_form": False
        },
        {
            "name": "priority",
            "type": "string",
            "validates": {"presence": True},
            "include_in_form": True,
            "options": ["Low", "Medium", "High"]  # Dropdown options for priority column
        },
        {
            "name": "request_details",
            "type": "string",
            "length": 255,
            "include_in_form": True
        }
    ]
}





        dynamic_model = self.create_dynamic_model(self.model_json)
        self.show_form(dynamic_model)

    def create_dynamic_model(self, model_json):
        metadata = MetaData()
        table_args = model_json.get('table_args', {})
        table = Table(model_json['table_name'], metadata, *[
            Column(col['name'], self.get_column_type(col), primary_key=col.get('primary_key', False), default=col.get('default', ''))
            for col in model_json['table_columns']
        ], **table_args)
        metadata.create_all(self.engine)
        return table

    def get_column_type(self, col_json):
        col_type = col_json['type']
        if col_type == 'string':
            return String(col_json.get('length', 255))
        elif col_type == 'integer':
            return Integer()
        # Add more types as needed
        else:
            raise ValueError(f"Unknown column type: {col_type}")

    def show_form(self, model):
        allowed_columns = []
        dropdown_columns = []
        for col in self.model_json['table_columns']:
            allowed_columns.append(col['name'])
            if 'options' in col:
                dropdown_columns.append(col['name'])  # Add column name directly

        form = FormWindow(model, self.session, allowed_columns, dropdown_columns, self.model_json)
        form.exec()


class FormWindow(QDialog):
    def __init__(self, model, session, allowed_columns, dropdown_columns, model_json):
        super().__init__()

        self.setWindowTitle(model.name)
        self.session = session
        self.model = model
        self.allowed_columns = allowed_columns
        self.dropdown_columns = dropdown_columns
        self.model_json = model_json

        layout = QFormLayout(self)
        self.setLayout(layout)

        self.fields = {}
        for col in model.columns:
            if col.name in self.allowed_columns:
                # Check if column is included in the form
                column_json = next((c for c in self.model_json['table_columns'] if c['name'] == col.name), None)
                if column_json and column_json.get("include_in_form", False):
                    label = QLabel(col.name)
                    if col.name in self.dropdown_columns:
                        try:
                            options = column_json['options']
                            print(f"Options found for column '{col.name}': {options}")
                            field = QComboBox()
                            field.addItems(options)
                        except KeyError:
                            print(f"Error: 'options' key not found for column '{col.name}'")
                            field = QLineEdit()  # Fallback to QLineEdit if options are missing
                    else:
                        field = QLineEdit()
                    layout.addRow(label, field)
                    self.fields[col.name] = field

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def accept(self):
        data = {name: field.currentText() if isinstance(field, QComboBox) else field.text() for name, field in self.fields.items()}
        insert_data = {col.name: data[col.name] for col in self.model.columns if col.name in self.allowed_columns}
        self.session.execute(self.model.insert().values(**insert_data))
        self.session.commit()
        super().accept()




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
