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

# Define the table and date range
table_name = 'transaction_table'
start_date = '2023-03-01'
end_date = '2023-03-31'

# Get the list of fields for the specified table
cursor = conn.cursor()
cursor.execute(f"SELECT COLUMN_NAME, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
fields = cursor.fetchall()

# Loop through each field
for field_name, byte_length in fields:
    # Loop through each byte position
    for byte_position in range(1, byte_length + 1):
        # Construct and execute the query to count byte occurrences
        query = f"SELECT BYTE_SUBSTR({field_name}, {byte_position}, 1) AS byte_value, COUNT(*) AS occurrence_count FROM {table_name} WHERE transaction_date BETWEEN '{start_date}' AND '{end_date}' GROUP BY byte_value ORDER BY byte_value"
        cursor.execute(query)
        results = cursor.fetchall()
        # Process the results (e.g., print them or store them in a data structure)
        print(f"Field: {field_name}, Byte Position: {byte_position}, Results: {results}")

# Close the connection
cursor.close()
conn.close()
