import json
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDateTimeEdit
from PyQt6.QtCore import QDateTime, QDate
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QTimer

class DependencyHandler:
    def __init__(self):
        self.dependent_fields = {}

    def setup_dependencies(self, fields, columns, is_json=False):
        for column in columns:
            # Choose the appropriate field name key based on whether it's a JSON column or not
            field_name_key = "json_column_name" if is_json else "name"
            field_name = column.get(field_name_key)

            # Skip if the field name is not present or the field should not be displayed
            if not field_name or not self.should_display_field(column.get('forms', [])):
                continue

            field_name = column["json_column_name"] if is_json else column["name"]
            for validator in column.get('validates', []):
                if validator['validation_type'] == 'valid_values_if_column_equals' and 'column_value_pairs' in validator:
                    dependent_field = fields.get(field_name)
                    if dependent_field is None:
                        continue

                    for pair in validator['column_value_pairs']:
                        target_field_name = pair['column_name']
                        # If it's a JSON field, the target field should be in the main form's fields.
                        target_field = self.fields.get(target_field_name) if is_json else fields.get(target_field_name)
                        if target_field:
                            self.dependent_fields.setdefault(target_field_name, []).append((dependent_field, pair))
                            # Connect only if not already connected to avoid multiple connections.
                            if not target_field.signalsBlocked():
                                target_field.currentTextChanged.connect(self.update_dependent_fields)



    def update_dependent_fields(self, value):
        sender = self.sender()
        field_name = None
        for key, field in self.fields.items():
            if field == sender:
                field_name = key
                break

        if not field_name:
            # If not found, search in JSON fields.
            for group in self.json_field_groups:
                for key, field in group.fields.items():
                    if field == sender:
                        field_name = key
                        break
                if field_name:
                    break

        if field_name and field_name in self.dependent_fields:
            for dependent_field, pair in self.dependent_fields[field_name]:
                if value == pair['column_value']:
                    dependent_field.clear()
                    dependent_field.addItems(pair['valid_values'])


    def create_field(self, field_type, column):
        field = None  # Initialize field to None

        if isinstance(column, dict):
            # Check for a 'valid_values' validation type
            if any(validator['validation_type'] == 'valid_values' for validator in column.get('validates', [])):
                valid_values_validator = next((validator for validator in column['validates'] if validator['validation_type'] == 'valid_values'), None)
                field = QtWidgets.QComboBox()
                field.addItems(valid_values_validator['valid_values'])

            # Check for a 'date' validation type
            elif any(validator['validation_type'] == 'date' for validator in column.get('validates', [])):
                date_validator = next((v for v in column['validates'] if v['validation_type'] == 'date'), None)
                field = QDateEdit()
                field.setCalendarPopup(True)
                qt_date_format = date_validator['date_format'].replace('YYYY', 'yyyy').replace('DD', 'dd')
                field.setDisplayFormat(qt_date_format)
                if date_validator.get('equal_current_date', False):
                    field.setDate(QDate.currentDate())

            # Check for a 'datetime' validation type
            elif any(validator['validation_type'] == 'datetime' for validator in column.get('validates', [])):
                field = QDateTimeEdit()
                field.setCalendarPopup(True)
                field.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
                if isinstance(column.get('default'), dict) and column['default'].get('has_default', False):
                    default_value = column['default'].get('default_value', QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"))
                    field.setDateTime(QDateTime.fromString(default_value, "yyyy-MM-dd HH:mm:ss"))
                else:
                    field.setDateTime(QDateTime.currentDateTime())

        # Handle the rest of the field types
        if field_type == "string" and field is None:
            # Check if there are specific validations for the field that require a combo box
            if any(validator['validation_type'] == 'valid_values_if_column_equals' for validator in column.get('validates', [])):
                field = QtWidgets.QComboBox()  # Create a combo box
                # Possibly populate with initial values if necessary
            else:
                field = QtWidgets.QLineEdit()  # Create a line edit as default for strings

        elif field_type == "numeric" and field is None:
            field = QtWidgets.QSpinBox()
            field.setRange(0, 100)  # Set your range as needed

        return field  # Always return the field

class JsonFieldGroup(QtWidgets.QWidget, DependencyHandler):
    def __init__(self, group_name, json_columns, should_display_field, main_fields, parent=None):
        super().__init__(parent)
        self.group_name = group_name
        self.json_columns = json_columns
        self.should_display_field = should_display_field
        self.main_fields = main_fields  # Store the main form fields
        self.dependent_fields = {}
        self.initUI()
        # Set up dependencies for JSON fields, passing in the main form fields as context
        self.setup_dependencies(self.fields, json_columns, is_json=True)

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.fields = {}
        for json_column in self.json_columns:
            if self.should_display_field(json_column):  # Use the passed method to check if the field should be displayed
                field_name = json_column["json_column_name"]
                field_type = json_column["type"]["type"]
                # Create label
                label = QtWidgets.QLabel(field_name)
                # Create field
                field = self.create_field(field_type, json_column)
                self.fields[field_name] = field
                self.layout.addWidget(label)
                self.layout.addWidget(field)
        self.setLayout(self.layout)
        self.setup_dependencies(self.fields, self.json_columns)
        self.trigger_initial_updates()  # Trigger initial updates for JSON fields

    def trigger_initial_updates(self):
        # Delay the update until the event loop starts
        QTimer.singleShot(0, self.initial_updates)

    def initial_updates(self):
        # Loop through each field that has dependencies and trigger the initial updates
        for master_field_name, dependencies in self.dependent_fields.items():
            master_field = self.fields.get(master_field_name)
            if isinstance(master_field, QtWidgets.QComboBox):
                # Set the initial values for dependent fields
                current_value = master_field.currentText()
                for dependent_field, pair in dependencies:
                    if current_value == pair['column_value']:
                        dependent_field.clear()
                        dependent_field.addItems(pair['valid_values'])

    def populate_json_fields(self, json_data):
        for data in json_data:
            for key, value in data.items():
                field = self.fields.get(key)
                if field:
                    if isinstance(field, QtWidgets.QLineEdit):
                        field.setText(str(value))
                    elif isinstance(field, QtWidgets.QComboBox):
                        index = field.findText(str(value))
                        if index >= 0:
                            field.setCurrentIndex(index)
                    elif isinstance(field, QtWidgets.QSpinBox):
                        field.setValue(int(value))

    def get_data(self):
        data = {}
        for name, field in self.fields.items():
            if isinstance(field, QtWidgets.QLineEdit):
                data[name] = field.text()
            elif isinstance(field, QtWidgets.QComboBox):
                data[name] = field.currentText()
            elif isinstance(field, QtWidgets.QSpinBox):
                data[name] = field.value()
            elif isinstance(field, (QDateEdit, QDateTimeEdit)):
                data[name] = field.dateTime().toString(field.displayFormat())
        return data




class DynamicForm(QtWidgets.QWidget, DependencyHandler):
    submitted = QtCore.pyqtSignal(dict)

    def __init__(self, column_definitions, data=None, form_name='defaultForm', parent=None):
        super().__init__(parent)
        self.column_definitions = column_definitions
        self.current_form_name = form_name
        self.data = data or {}
        self.json_field_groups = []  # Initialize the attribute here
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QFormLayout()
        self.fields = {}

        for column in self.column_definitions:
            if self.should_display_field(column):
                field_name = column["name"]
                field_type = column["type"]["type"]
                if field_type in ["string", "numeric"]:
                    self.fields[field_name] = self.create_field(field_type, column)
                elif field_type == "json":
                    self.fields[field_name] = self.create_json_field(column)

                self.layout.addRow(field_name, self.fields[field_name])

                # Set the enabled state based on the 'editable' property
                editable = self.is_field_editable(column)
                self.fields[field_name].setEnabled(editable)

        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addRow(self.submit_button)
        self.setLayout(self.layout)

        # Setup dependencies and trigger initial updates
        self.setup_dependencies(self.fields, self.column_definitions)
        self.trigger_initial_updates()


    def is_field_editable(self, column):
        form_settings = column.get('forms', [])
        for form_info in form_settings:
            if form_info['form_name'] == self.current_form_name:
                return form_info.get('editable', False)
        return False

    def should_display_field(self, column):
        if isinstance(column, dict):
            form_settings = column.get('forms', [])
            for form_info in form_settings:
                if form_info['form_name'] == self.current_form_name:
                    return True
        elif isinstance(column, list):
            # Assume it's a list of form settings directly
            for form_info in column:
                if form_info['form_name'] == self.current_form_name:
                    return True
        return False



    def trigger_initial_updates(self):
        # Delay the update until the event loop starts
        QTimer.singleShot(0, self.initial_updates)

    def initial_updates(self):
        # Loop through each field that has dependencies and trigger the initial updates
        for master_field_name, dependencies in self.dependent_fields.items():
            master_field = self.fields.get(master_field_name)
            if isinstance(master_field, QtWidgets.QComboBox):
                # Set the initial values for dependent fields
                current_value = master_field.currentText()
                for dependent_field, pair in dependencies:
                    if current_value == pair['column_value']:
                        dependent_field.clear()
                        dependent_field.addItems(pair['valid_values'])

    def create_json_field(self, column):
        json_group_name = column["name"]
        json_columns = column["json_columns"]
        json_layout = QtWidgets.QVBoxLayout()

        add_button = QtWidgets.QPushButton(f"Add {json_group_name}")
        json_layout.addWidget(add_button)

        # Create a function to add a new JsonFieldGroup
        def add_json_field_group():
            group = JsonFieldGroup(json_group_name, json_columns, self.should_display_field, self.fields)
            group.setup_dependencies(group.fields, json_columns, is_json=True)
            self.json_field_groups.append(group)
            group_box = QtWidgets.QGroupBox(f"{json_group_name} Details")
            group_layout = QtWidgets.QVBoxLayout(group_box)
            group_layout.addWidget(group)
            remove_button = QtWidgets.QPushButton(f"Remove {json_group_name}")
            remove_button.clicked.connect(lambda: self.remove_json_field_group(group_box))
            group_layout.addWidget(remove_button)
            json_layout.addWidget(group_box)

        # Create and add the first JsonFieldGroup
        add_json_field_group()

        # Create an "Add" button to add more JsonFieldGroups
        add_button.clicked.connect(add_json_field_group)

        # Create a QGroupBox to contain the JsonFieldGroups and the "Add" button
        json_group_box = QtWidgets.QGroupBox(json_group_name)
        json_group_box.setLayout(json_layout)

        return json_group_box

    def add_json_field_group(self, group_name, json_columns):
        group = JsonFieldGroup(group_name, json_columns, self.should_display_field)  # Pass the method reference
        self.json_field_groups.append(group)
        group_box = QtWidgets.QGroupBox(f"{group_name} Details")
        group_layout = QtWidgets.QVBoxLayout(group_box)
        group_layout.addWidget(group)
        remove_button = QtWidgets.QPushButton(f"Remove {group_name}")
        remove_button.clicked.connect(lambda: self.remove_json_field_group(group_box))
        group_layout.addWidget(remove_button)
        self.json_layout.addWidget(group_box)

    def remove_json_field_group(self, group_box):
        # Remove the entire QGroupBox, not just the JsonFieldGroup
        self.json_field_groups.remove(group_box.findChild(JsonFieldGroup))
        group_box.deleteLater()
                    
    def submit(self):
        # Collect data for regular fields
        regular_data = {}
        for name, widget in self.fields.items():
            if not isinstance(widget, QtWidgets.QGroupBox):
                if isinstance(widget, QtWidgets.QLineEdit):
                    regular_data[name] = widget.text()
                elif isinstance(widget, QtWidgets.QComboBox):
                    regular_data[name] = widget.currentText()
                elif isinstance(widget, QtWidgets.QSpinBox):
                    regular_data[name] = widget.value()
                elif isinstance(widget, (QDateEdit, QDateTimeEdit)):
                    regular_data[name] = widget.dateTime().toString(widget.displayFormat())

        # Collect data for JSON fields
        json_data = [group.get_data() for group in self.json_field_groups]

        # Combine regular fields data with JSON fields data
        self.data = {**regular_data, 'user_json': json_data}

        print(self.data)
        self.submitted.emit(self.data)
        self.close()



# Example usage
app = QtWidgets.QApplication([])

# Load appConfigurations JSON
with open('test.json') as file:
    model_json = json.load(file)
    
form = DynamicForm(model_json["table_columns"])
form.show()
app.exec()