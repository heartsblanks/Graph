import sqlite3
import csv
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name='example.db'):
        self.db_name = db_name

    def create_table(self, cursor, table_name, columns):
        columns_sql = ', '.join([f'"{col}" TEXT' for col in columns])
        create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql})'
        cursor.execute(create_table_sql)

    def load_data_into_table(self, cursor, table_name, cleaned_file, columns, delimiter=';'):
        with open(cleaned_file, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            next(reader)  # Skip header
            placeholders = ', '.join(['?' for _ in columns])
            insert_sql = f'INSERT INTO "{table_name}" ({", ".join(columns)}) VALUES ({placeholders})'
            for row in reader:
                cursor.execute(insert_sql, row)

    def create_database_and_load_data(self, cleaned_file1, cleaned_file2, columns_table1, columns_table2, delimiter=';'):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create tables using dynamic column names
        self.create_table(cursor, 'table1', columns_table1)
        self.create_table(cursor, 'table2', columns_table2)

        # Load data into tables
        self.load_data_into_table(cursor, 'table1', cleaned_file1, columns_table1, delimiter)
        self.load_data_into_table(cursor, 'table2', cleaned_file2, columns_table2, delimiter)

        conn.commit()
        conn.close()

    def query_database(self, query, params=()):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def get_coordinates(self):
        conn = sqlite3.connect(self.db_name)
        query = 'SELECT A FROM table1 UNION SELECT A FROM table2'
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Generate coordinates
        df['x'] = df.index % 50 * 20  # Adjust as needed
        df['y'] = df.index // 50 * 20 # Adjust as needed
        return df[['x', 'y']].to_dict(orient='records')