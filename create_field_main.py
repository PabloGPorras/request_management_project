    def create_field(self, field_type, column):
        if isinstance(column, dict):
            # Check for a 'valid_values' validation type
            if any(validator['validation_type'] == 'valid_values' for validator in column.get('validates', [])):
                valid_values_validator = next((validator for validator in column['validates'] if validator['validation_type'] == 'valid_values'), None)
                field = QtWidgets.QComboBox()
                field.addItems(valid_values_validator['valid_values'])
                return field

            # Check for a 'date' validation type
            if any(validator['validation_type'] == 'date' for validator in column.get('validates', [])):
                date_validator = next((v for v in column['validates'] if v['validation_type'] == 'date'), None)
                field = QDateEdit()
                field.setCalendarPopup(True)

                # Set the display format based on the 'date_format' in the validator
                # Conversion from Python's strftime to Qt's format might be needed
                qt_date_format = date_validator['date_format'].replace('YYYY', 'yyyy').replace('DD', 'dd')
                field.setDisplayFormat(qt_date_format)

                # Set the date to the current date if 'equal_current_date' is True
                if date_validator.get('equal_current_date', False):
                    field.setDate(QDate.currentDate())

                return field
            
            # Check for a 'datetime' validation type
            if any(validator['validation_type'] == 'datetime' for validator in column.get('validates', [])):
                field = QDateTimeEdit()
                field.setCalendarPopup(True)
                field.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Adjust the format as needed

                # Check if there's a default value
                if isinstance(column.get('default'), dict) and column['default'].get('has_default', False):
                    default_value = column['default'].get('default_value', QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"))
                    field.setDateTime(QDateTime.fromString(default_value, "yyyy-MM-dd HH:mm:ss"))
                else:
                    field.setDateTime(QDateTime.currentDateTime())
                return field