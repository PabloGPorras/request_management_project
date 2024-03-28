import json
from sqlalchemy import inspect
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import validates
from database.engine import getEngine
from datetime import datetime
  
class ModelBuilder:
    def __init__(self, metadata):
        self.metadata = metadata

    def create_model(self, table_name, columns):
        column_objs = []
        for column in columns:
            column_name = column["name"]
            column_type = self.get_column_type(column["type"])
            column_obj = Column(column_name, column_type, primary_key=column.get("primary_key", False))
            column_objs.append(column_obj)

            for validator in column.get("validates", []):
                validation_func = self.make_validator(column_name, validator)
                setattr(self, f"validate_{column_name}", validation_func)

        table = Table(table_name, self.metadata, *column_objs)
        return table

    def get_column_type(self, column_type):
        if column_type["type"] in ("string","json"):
            return String(length=column_type["length"])
        elif column_type["type"] == "numeric":
            return Numeric()

    def make_validator(self, column_name, validator):
        validation_type = validator["validation_type"]
        if validation_type == "string_length":
            return self.make_string_length_validator(column_name, validator)
        elif validation_type == "valid_values":
            return self.make_valid_values_validator(column_name, validator)
        elif validation_type == "datetime":
            return self.make_datetime_validator(column_name, validator)
        elif validation_type == "date":
            return self.make_date_validator(column_name, validator)
        elif validation_type == "numeric_range":
            return self.make_numeric_range_validator(column_name, validator)
        elif validation_type == "time":
            return self.make_time_validator(column_name, validator)
        elif validation_type == "valid_values_if_column_equals":
            return self.make_valid_values_if_column_equals_validator(column_name, validator)

    def make_string_length_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            min_length = validator.get("min_length", None)
            max_length = validator.get("max_length", None)
            if min_length is not None and len(value) < min_length:
                raise Exception(validator["error_message"])
            if max_length is not None and len(value) > max_length:
                raise Exception(validator["error_message"])
            return value
        return validator_func

    def make_valid_values_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            valid_values = validator["valid_values"]
            if value not in valid_values:
                raise Exception(f"Invalid value {value} not in {valid_values}")
            return value
        return validator_func

    def make_datetime_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            min_date_str = validator.get("min_date", None)
            max_date_str = validator.get("max_date", None)
            if min_date_str is not None:
                min_date = datetime.strptime(min_date_str, validator["datetime_format"])
                if value < min_date:
                    raise Exception("Date is too early")
            if max_date_str is not None:
                max_date = datetime.strptime(max_date_str, validator["datetime_format"])
                if value > max_date:
                    raise Exception("Date is too late")
            return value
        return validator_func

    def make_date_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            # Implement date validator logic here
            return value
        return validator_func

    def make_numeric_range_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            # Implement numeric range validator logic here
            return value
        return validator_func

    def make_time_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            # Implement time validator logic here
            return value
        return validator_func

    def make_valid_values_if_column_equals_validator(self, column_name, validator):
        @validates(column_name)
        def validator_func(self, key, value):
            column_value_pairs = validator["column_value_pairs"]
            for pair in column_value_pairs:
                if pair["column_name"] == column_name and value == pair["column_value"]:
                    valid_values = pair["valid_values"]
                    if value not in valid_values:
                        raise Exception("Invalid value")
                    break
            else:
                # Column value pair not found, value is valid
                return value
        return validator_func

    def make_position_numeric_validator(self, column_name, validator):
        positions = validator.get("positions", [])
        @validates(column_name)
        def validator_func(self, key, value):
            for pos in positions:
                if not value[pos].isdigit():
                    raise Exception(f"Position {pos} must be numeric")
            return value
        return validator_func

    def make_position_character_validator(self, column_name, validator):
        positions = validator.get("positions", [])
        @validates(column_name)
        def validator_func(self, key, value):
            for pos in positions:
                if not value[pos].isalpha():
                    raise Exception(f"Position {pos} must be a character")
            return value
        return validator_func

    def validate_data(self, table, data):
        for column_name, value in data.items():
            validate_func = getattr(self, f"validate_{column_name}", None)
            if validate_func:
                validated_value = validate_func(self, column_name, value)
                data[column_name] = validated_value
        return data