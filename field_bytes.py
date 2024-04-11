import snowflake.connector

# Connect to Snowflake
conn = snowflake.connector.connect(
    user='your_username',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='your_schema'
)

# Define the table
table_name = 'transaction_table'

# Create a result table in Snowflake
conn.cursor().execute(
    """
    CREATE OR REPLACE TABLE empty_char_positions (
        field_name VARCHAR(255),
        char_position INT
    )
    """
)

# Fetch the list of string fields
fields = conn.cursor().execute(
    f"""
    SELECT COLUMN_NAME, CHARACTER_MAXIMUM_LENGTH
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}'
    AND DATA_TYPE LIKE '%CHAR%'  -- Assuming you're interested in string fields
    """
).fetchall()

# Loop through fields and character positions
for field_name, char_length in fields:
    if char_length is not None:
        for char_position in range(1, char_length + 1):
            # Construct the query to find empty characters
            query = (
                f"INSERT INTO empty_char_positions (field_name, char_position) "
                f"SELECT '{field_name}' AS field_name, {char_position} AS char_position "
                f"FROM {table_name} "
                f"WHERE SUBSTR({field_name}, {char_position}, 1) = ' '"
            )
            # Execute the query
            conn.cursor().execute(query)

# Close the connection
conn.close()
