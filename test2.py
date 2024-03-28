import json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import validates
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
                setattr(self, f"validate_{column_name}_{validator['validation_type']}", validation_func)

        table = Table(table_name, self.metadata, *column_objs)
        return table

    def get_column_type(self, column_type):
        if column_type["type"] == "string":
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
                raise Exception("Invalid value")
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
    
# Example JSON data for creating a model
with open('test.json', 'r') as file:
    model_json = json.load(file)


# Create SQLAlchemy engine and metadata
engine = create_engine("sqlite:///database2.db")
metadata = MetaData(bind=engine)

# Create model using ModelBuilder
model_builder = ModelBuilder(metadata)
user_table = model_builder.create_model(model_json["table_name"], model_json["table_columns"])

# Create all tables in the database
metadata.create_all()

# Check if table is created successfully
print(engine.has_table("users"))


bad_data = {
    'user_id': 2,  # should be numeric
    'user_name': 'short',  # should be between 10 and 20 characters
    'user_role': 'invalid_role',  # should be 'user', 'manager', or 'admin'
    'user_created_datetime': '2020-01-01 10:00:00',  # should be between 2018-01-01 and 2018-12-31
    'user_last_login_date': '2022-01-01',  # should be equal to the current date
    'user_login_count': 10000,  # should be between 1 and 9999
    'user_business_unit': 'invalid_unit',  # should be 'credit', 'debit', 'loan', or 'mortgage'
    'user_teams': 'invalid_team',  # should be a valid team based on 'user_business_unit'
    'random_column_name': 'invalid_value'  # should satisfy multiple validation rules
}

# Validate the bad data before inserting
for column_name, value in bad_data.items():
    validate_func = getattr(model_builder, f"validate_{column_name}", None)
    if validate_func:
        try:
            validated_value = validate_func(model_builder, column_name, value)
        except Exception as e:
            print(f"Validation failed for column '{column_name}': {e}")
        else:
            print(f"Validation passed for column '{column_name}': {validated_value}")
    else:
        print(f"No validator found for column '{column_name}'")

query = user_table.insert().values(bad_data)
with engine.connect() as connection:
    result = connection.execute(query)