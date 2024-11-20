import pandas as pd
import sqlite3
import os

# Combined CSV file path
csv_file = "movies_cleaned.csv"  # Replace with your file path

# SQLite database path
db_file = "test.db"  # Replace with your desired database file path

# Table name
table_name = "movie_info"

# Load the CSV file
data = pd.read_csv(csv_file)

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect(db_file)

# Save DataFrame to SQLite database
data.to_sql(table_name, conn, if_exists="replace", index=False)

# Confirm data insertion
print(f"Data successfully inserted into the SQLite database: {db_file}, table: {table_name}")

# Close the database connection
conn.close()
