import os
import re
import sqlite3

# Directory containing .properties files
folder_path = 'path/to/your/folder'

# Database setup
db_name = 'queue_details.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create table in SQLite database
cursor.execute('''
CREATE TABLE IF NOT EXISTS QUEUE_DETAILS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_queue TEXT,
    copy_queue TEXT,
    error_queue TEXT,
    business_error_queue TEXT,
    output_queue TEXT,
    process_id TEXT,
    category TEXT
)
''')

# Define regular expressions for the required keys
patterns = {
    'input_queue': re.compile(r'^replace\.replacement\.10\s*=\s*(.*)$', re.MULTILINE),
    'copy_queue': re.compile(r'^replace\.replacement\.11\s*=\s*(.*)$', re.MULTILINE),
    'error_queue': re.compile(r'^replace\.replacement\.12\s*=\s*(.*)$', re.MULTILINE),
    'output_queue': re.compile(r'^replace\.replacement\.18\s*=\s*(.*)$', re.MULTILINE),
    'business_error_queue': re.compile(r'^replace\.replacement\.24\s*=\s*(.*)$', re.MULTILINE),
    'process_id': re.compile(r'^replace\.replacement\.5\s*=\s*(.*)$', re.MULTILINE),
    'category': re.compile(r'^replace\.replacement\.7\s*=\s*(.*)$', re.MULTILINE),
}

# Data insertion
for filename in os.listdir(folder_path):
    if filename.endswith('.properties'):
        file_path = os.path.join(folder_path, filename)

        # Read the entire file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Extract values using regular expressions
        record = {key: None for key in patterns}
        for key, pattern in patterns.items():
            match = pattern.search(content)
            if match:
                record[key] = match.group(1).strip()
        
        # Insert the record into the database
        cursor.execute('''
        INSERT INTO QUEUE_DETAILS (
            input_queue, copy_queue, error_queue, business_error_queue,
            output_queue, process_id, category
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['input_queue'], record['copy_queue'], record['error_queue'],
            record['business_error_queue'], record['output_queue'],
            record['process_id'], record['category']
        ))

# Commit and close the connection
conn.commit()
conn.close()

print("Data extraction and table creation completed. The data is stored in queue_details.db.")