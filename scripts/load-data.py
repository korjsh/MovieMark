import pandas as pd
import sqlite3
import os

print("Current working directory:", os.getcwd())

# Base directory of the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# File paths
csv_file = os.path.join(base_dir, "data", "top_100_movies_titles.csv")
db_file = os.path.join(base_dir, "..", "dist", "test.db")  # Adjust as needed

# Table name
table_name = "movies"

# Load the CSV file
data = pd.read_csv(csv_file)

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect(db_file)

# Save DataFrame to SQLite database
data.to_sql(table_name, conn, if_exists="replace", index=False)

# Confirm data insertion
print(
    f"Data successfully inserted into the SQLite database: {db_file}, table: {table_name}"
)

# Close the database connection
conn.close()
