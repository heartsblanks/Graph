
import sqlite3
import pandas as pd

# Load the CSV files into pandas DataFrames
table1 = pd.read_csv('table1.csv')
table2 = pd.read_csv('table2.csv')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Load data into the database (replace the tables if they already exist)
table1.to_sql('table1', conn, if_exists='replace', index=False)
table2.to_sql('table2', conn, if_exists='replace', index=False)

# Get unique values from Column A from both tables
unique_values_column_a = pd.concat([table1['A'], table2['A']]).unique()

conn.close()