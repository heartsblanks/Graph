import os
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

# Data insertion
for filename in os.listdir(folder_path):
    if filename.endswith('.properties'):
        file_path = os.path.join(folder_path, filename)
        
        # Read the file and extract values
        try:
            record = {
                'input_queue': None,
                'copy_queue': None,
                'error_queue': None,
                'business_error_queue': None,
                'output_queue': None,
                'process_id': None,
                'category': None
            }
            
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith('replace.replacement.'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == 'replace.replacement.10':
                            record['input_queue'] = value
                        elif key == 'replace.replacement.11':
                            record['copy_queue'] = value
                        elif key == 'replace.replacement.12':
                            record['error_queue'] = value
                        elif key == 'replace.replacement.18':
                            record['output_queue'] = value
                        elif key == 'replace.replacement.24':
                            record['business_error_queue'] = value
                        elif key == 'replace.replacement.5':
                            record['process_id'] = value
                        elif key == 'replace.replacement.7':
                            record['category'] = value

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