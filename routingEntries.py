                    import sqlite3
import csv
from datetime import datetime

# Database name
db_name = 'FLOWCEPTION.db'

def extract_pap_name(target):
    parts = target.split('_')
    if len(parts) > 2:
        return parts[2]  # PAP name is between the 2nd and 3rd underscore
    return None

def load_routing_entries_from_csv(cleaned_file1, cleaned_file2, delimiter=';'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Load data from cleaned_file1 into ROUTING_ENTRIES
    with open(cleaned_file1, 'r') as file1:
        reader = csv.DictReader(file1, delimiter=delimiter)
        for row in reader:
            # Strip whitespace from all fields
            process_id = row['PROCESS_ID'].strip()
            category = row['CATEGORY'].strip()
            target_tp = row['TARGET_TP'].strip()
            target = row['TARGET'].strip()
            additional_data = row['ADDITIONAL_DATA'].strip()

            if row['GLT_VON'].strip() <= current_time <= row['GLT_BIS'].strip():
                # Extract PAP name from TARGET
                target_pap = extract_pap_name(target)

                # Query for INPUT_QUEUE based on PROCESS_ID and CATEGORY
                cursor.execute('''
                SELECT REPLACE_REPLACEMENT_10
                FROM QUEUE_DETAILS
                WHERE PROCESS_ID = ? AND CATEGORY = ?
                ''', (process_id, category))
                input_queue = cursor.fetchone()
                input_queue = input_queue[0] if input_queue else None

                # Insert into ROUTING_ENTRIES
                cursor.execute('''
                    INSERT INTO ROUTING_ENTRIES (
                        PROCESS_ID, INPUT_QUEUE, CATEGORY, ROUTING_ID_1, ROUTING_ID_2, ROUTING_ID_3,
                        ROUTING_ID_4, ROUTING_ID_5, ROUTING_ID_6, ROUTING_ID_7, ROUTING_ID_8,
                        ROUTING_ID_9, ROUTING_ID_10, ROUTING_ID_11, ROUTING_ID_12, ROUTING_ID_13,
                        ROUTING_ID_14, ROUTING_ID_15, ROUTING_ID_16, ROUTING_ID_17, ROUTING_ID_18,
                        ROUTING_ID_19, ROUTING_ID_20, TARGET_TP, TARGET, ADDITIONAL_DATA,
                        TARGET_PAP, TARGET_PROCESS_ID
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    process_id, input_queue, category,
                    row['ROUTING_ID_1'].strip(), row['ROUTING_ID_2'].strip(), row['ROUTING_ID_3'].strip(),
                    row['ROUTING_ID_4'].strip(), row['ROUTING_ID_5'].strip(), row['ROUTING_ID_6'].strip(),
                    row['ROUTING_ID_7'].strip(), row['ROUTING_ID_8'].strip(), row['ROUTING_ID_9'].strip(),
                    row['ROUTING_ID_10'].strip(), row['ROUTING_ID_11'].strip(), row['ROUTING_ID_12'].strip(),
                    row['ROUTING_ID_13'].strip(), row['ROUTING_ID_14'].strip(), row['ROUTING_ID_15'].strip(),
                    row['ROUTING_ID_16'].strip(), row['ROUTING_ID_17'].strip(), row['ROUTING_ID_18'].strip(),
                    row['ROUTING_ID_19'].strip(), row['ROUTING_ID_20'].strip(), target_tp, target, additional_data,
                    target_pap, None  # Initial value for TARGET_PROCESS_ID
                ))

    # Load data from cleaned_file2 into ROUTING_ENTRIES (without routing IDs)
    with open(cleaned_file2, 'r') as file2:
        reader = csv.DictReader(file2, delimiter=delimiter)
        for row in reader:
            # Strip whitespace from all fields
            process_id = row['PROCESS_ID'].strip()
            category = row['CATEGORY'].strip()
            target_tp = row['TARGET_TP'].strip()
            target = row['TARGET'].strip()
            additional_data = row['ADDITIONAL_DATA'].strip()

            if row['GLT_VON'].strip() <= current_time <= row['GLT_BIS'].strip():
                # Extract PAP name from TARGET
                target_pap = extract_pap_name(target)

                # Query for INPUT_QUEUE based on PROCESS_ID and CATEGORY
                cursor.execute('''
                SELECT REPLACE_REPLACEMENT_10
                FROM QUEUE_DETAILS
                WHERE PROCESS_ID = ? AND CATEGORY = ?
                ''', (process_id, category))
                input_queue = cursor.fetchone()
                input_queue = input_queue[0] if input_queue else None

                # Insert into ROUTING_ENTRIES (without routing IDs)
                cursor.execute('''
                    INSERT INTO ROUTING_ENTRIES (
                        PROCESS_ID, INPUT_QUEUE, CATEGORY, TARGET_TP, TARGET, ADDITIONAL_DATA,
                        TARGET_PAP, TARGET_PROCESS_ID
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    process_id, input_queue, category, target_tp, target, additional_data,
                    target_pap, None  # Initial value for TARGET_PROCESS_ID
                ))

    # Update TARGET_PROCESS_ID by matching TARGET_PAP with QUEUE_DETAILS
    cursor.execute('''
    UPDATE ROUTING_ENTRIES
    SET TARGET_PROCESS_ID = (
        SELECT PROCESS_ID
        FROM QUEUE_DETAILS
        WHERE QUEUE_DETAILS.TARGET = ROUTING_ENTRIES.TARGET
    )
    ''')

    conn.commit()
    conn.close()

# Paths to cleaned CSV files
cleaned_file1 = 'path_to_cleaned_file1.csv'
cleaned_file2 = 'path_to_cleaned_file2.csv'

# Load data from the CSV files into the database
if __name__ == "__main__":
    load_routing_entries_from_csv(cleaned_file1, cleaned_file2)
    print("Data loaded into ROUTING_ENTRIES table.")