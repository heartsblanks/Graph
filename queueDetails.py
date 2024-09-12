import os
import sqlite3
from configparser import ConfigParser

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

# Data insertion
for filename in os.listdir(folder_path):
    if filename.endswith('.properties'):
        file_path = os.path.join(folder_path, filename)
        
        # Create a ConfigParser object and read the file
        config = ConfigParser()
        config.read(file_path)
        
        # Extract values from the file
        try:
            record = {
                'input_queue': config.get('replace.replacement', '10', fallback=None),
                'copy_queue': config.get('replace.replacement', '11', fallback=None),
                'error_queue': config.get('replace.replacement', '12', fallback=None),
                'business_error_queue': config.get('replace.replacement', '24', fallback=None),
                'output_queue': config.get('replace.replacement', '18', fallback=None),
                'process_id': config.get('replace.replacement', '5', fallback=None),
                'category': config.get('replace.replacement', '7', fallback=None)
            }
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
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Commit and close the connection
conn.commit()
conn.close()

print("Data extraction and table creation completed. The data is stored in queue_details.db.")