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

# Create a result table in Snowflake
conn.cursor().execute(
    """
    CREATE OR REPLACE TABLE byte_analysis_results (
        field_name VARCHAR(255),
        byte_position INT,
        byte_value VARCHAR(1),
        occurrence_count INT
    )
    """
)

# Fetch the list of fields
fields = conn.cursor().execute(
    f"""
    SELECT COLUMN_NAME, CHARACTER_MAXIMUM_LENGTH
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{table_name}'
    """
).fetchall()

# Loop through fields and byte positions
for field_name, byte_length in fields:
    for byte_position in range(1, byte_length + 1):
        # Construct the query
        query = (
            f"INSERT INTO byte_analysis_results (field_name, byte_position, byte_value, occurrence_count) "
            f"SELECT '{field_name}' AS field_name, {byte_position} AS byte_position, BYTE_SUBSTR({field_name}, {byte_position}, 1) AS byte_value, COUNT(*) AS occurrence_count "
            f"FROM {table_name} "
            f"WHERE transaction_date BETWEEN '{start_date}' AND '{end_date}' "
            f"GROUP BY byte_value ORDER BY byte_value"
        )
        # Execute the query
        conn.cursor().execute(query)

# Close the connection
conn.close()
