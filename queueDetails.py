# queueDetails.py

import os
import sqlite3

# Database name
db_name = 'FLOWCEPTION.db'

# Function to fetch and insert/update queue details
def process_properties_files(directory):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Loop through all .properties files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.properties'):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r') as file:
                data = {}
                for line in file:
                    if line.startswith('replace.replacement.'):
                        key, value = line.split('=')
                        key = key.strip()
                        value = value.strip()

                        if key == 'replace.replacement.10':
                            data['INPUT_QUEUE'] = value if not value.startswith('CHANGE_') else None
                        elif key == 'replace.replacement.11':
                            data['COPY_QUEUE'] = value if not value.startswith('CHANGE_') else None
                        elif key == 'replace.replacement.12':
                            data['ERROR_QUEUE'] = value if not value.startswith('CHANGE_') else None
                        elif key == 'replace.replacement.24':
                            data['BUSINESS_ERROR_QUEUE'] = value if not value.startswith('CHANGE_') else None
                        elif key == 'replace.replacement.18':
                            data['OUTPUT_QUEUE'] = value if not value.startswith('CHANGE_') else None
                        elif key == 'replace.replacement.5':
                            data['PROCESS_ID'] = value
                            # Extract PAP (characters at position 3, 5-7)
                            data['PAP'] = value[2] + value[4:7] if len(value) >= 7 else None
                        elif key == 'replace.replacement.7':
                            data['CATEGORY'] = value

                # If all queues start with "CHANGE_", skip this entry
                if all(value is None for key, value in data.items() if 'QUEUE' in key):
                    continue

                # Use INSERT OR REPLACE to either insert a new row or replace the existing one
                cursor.execute('''
                INSERT OR REPLACE INTO QUEUE_DETAILS (
                    ID, INPUT_QUEUE, COPY_QUEUE, ERROR_QUEUE, BUSINESS_ERROR_QUEUE,
                    OUTPUT_QUEUE, PROCESS_ID, CATEGORY, PAP
                ) VALUES (
                    (SELECT ID FROM QUEUE_DETAILS WHERE PROCESS_ID = ? AND CATEGORY = ?),
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                ''', (
                    data.get('PROCESS_ID'),
                    data.get('CATEGORY'),
                    data.get('INPUT_QUEUE'),
                    data.get('COPY_QUEUE'),
                    data.get('ERROR_QUEUE'),
                    data.get('BUSINESS_ERROR_QUEUE'),
                    data.get('OUTPUT_QUEUE'),
                    data.get('PROCESS_ID'),
                    data.get('CATEGORY'),
                    data.get('PAP')
                ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Processed files in directory: {directory}")

# Specify the directory containing .properties files
directory_path = 'path_to_properties_files'

# Process the properties files
process_properties_files(directory_path)