import sqlite3

# Database name
db_name = 'FLOWCEPTION.db'

def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop ROUTING_ENTRIES table if it exists
    cursor.execute("DROP TABLE IF EXISTS ROUTING_ENTRIES")

    # Create ROUTING_ENTRIES table with the new column Target_Process_ID
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROUTING_ENTRIES (
        PROCESS_ID TEXT,
        CATEGORY TEXT,
        ROUTING_ID_1 TEXT, ROUTING_ID_2 TEXT, ROUTING_ID_3 TEXT,
        ROUTING_ID_4 TEXT, ROUTING_ID_5 TEXT, ROUTING_ID_6 TEXT,
        ROUTING_ID_7 TEXT, ROUTING_ID_8 TEXT, ROUTING_ID_9 TEXT,
        ROUTING_ID_10 TEXT, ROUTING_ID_11 TEXT, ROUTING_ID_12 TEXT,
        ROUTING_ID_13 TEXT, ROUTING_ID_14 TEXT, ROUTING_ID_15 TEXT,
        ROUTING_ID_16 TEXT, ROUTING_ID_17 TEXT, ROUTING_ID_18 TEXT,
        ROUTING_ID_19 TEXT, ROUTING_ID_20 TEXT,
        TARGET_TP TEXT,
        TARGET TEXT,
        ADDITIONAL_DATA TEXT,
        TARGET_PAP TEXT,
        TARGET_PROCESS_ID TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Call the function to create the database and table
if __name__ == "__main__":
    create_database()
    print("ROUTING_ENTRIES table created (if it didn't exist already).")