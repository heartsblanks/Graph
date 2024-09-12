import sqlite3
import csv
from datetime import datetime

# Database name
db_name = 'FLOWCEPTION.db'

# Function to load CSV data into ROUTING_ENTRIES table, filtered by GLT_VON and GLT_BIS
def load_routing_entries_from_csv(cleaned_file1, cleaned_file2, delimiter=';'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Load data from cleaned_file1 into ROUTING_ENTRIES
    with open(cleaned_file1, 'r') as file1:
        reader = csv.DictReader(file1, delimiter=delimiter)
        for row in reader:
            # Check if current timestamp is between GLT_VON and GLT_BIS
            if row['GLT_VON'] <= current_time <= row['GLT_BIS']:
                # Insert into ROUTING_ENTRIES, omitting GLT_VON and GLT_BIS
                cursor.execute('''
                    INSERT INTO ROUTING_ENTRIES (
                        PROCESS_ID, CATEGORY, ROUTING_ID_1, ROUTING_ID_2, ROUTING_ID_3,
                        ROUTING_ID_4, ROUTING_ID_5, ROUTING_ID_6, ROUTING_ID_7, ROUTING_ID_8,
                        ROUTING_ID_9, ROUTING_ID_10, ROUTING_ID_11, ROUTING_ID_12, ROUTING_ID_13,
                        ROUTING_ID_14, ROUTING_ID_15, ROUTING_ID_16, ROUTING_ID_17, ROUTING_ID_18,
                        ROUTING_ID_19, ROUTING_ID_20, TARGET_TP, TARGET, ADDITIONAL_DATA
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['PROCESS_ID'], row['CATEGORY'],
                    row['ROUTING_ID_1'], row['ROUTING_ID_2'], row['ROUTING_ID_3'],
                    row['ROUTING_ID_4'], row['ROUTING_ID_5'], row['ROUTING_ID_6'],
                    row['ROUTING_ID_7'], row['ROUTING_ID_8'], row['ROUTING_ID_9'],
                    row['ROUTING_ID_10'], row['ROUTING_ID_11'], row['ROUTING_ID_12'],
                    row['ROUTING_ID_13'], row['ROUTING_ID_14'], row['ROUTING_ID_15'],
                    row['ROUTING_ID_16'], row['ROUTING_ID_17'], row['ROUTING_ID_18'],
                    row['ROUTING_ID_19'], row['ROUTING_ID_20'], row['TARGET_TP'],
                    row['TARGET'], row['ADDITIONAL_DATA']
                ))

    # Load data from cleaned_file2 into ROUTING_ENTRIES (without routing IDs)
    with open(cleaned_file2, 'r') as file2:
        reader = csv.DictReader(file2, delimiter=delimiter)
        for row in reader:
            # Check if current timestamp is between GLT_VON and GLT_BIS
            if row['GLT_VON'] <= current_time <= row['GLT_BIS']:
                # Insert into ROUTING_ENTRIES (without routing IDs)
                cursor.execute('''
                    INSERT INTO ROUTING_ENTRIES (
                        PROCESS_ID, CATEGORY, TARGET_TP, TARGET, ADDITIONAL_DATA
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    row['PROCESS_ID'], row['CATEGORY'], row['TARGET_TP'], row['TARGET'], row['ADDITIONAL_DATA']
                ))

    conn.commit()
    conn.close()

# Paths to cleaned CSV files
cleaned_file1 = 'path_to_cleaned_file1.csv'
cleaned_file2 = 'path_to_cleaned_file2.csv'

# Load data from the CSV files into the database
if __name__ == "__main__":
    load_routing_entries_from_csv(cleaned_file1, cleaned_file2)
    print("Data loaded into ROUTING_ENTRIES table.")