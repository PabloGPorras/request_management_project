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
            field = QtWidgets.QLineEdit()
        elif field_type == "numeric" and field is None:
            field = QtWidgets.QSpinBox()
            field.setRange(0, 100)  # Set your range as needed

        return field  # Always return the field_