import sqlite3

# Funny database name
db_name = 'FLOWCEPTION.db'

# Connect to the database (will be created if it doesn't exist)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# --------------------------------------
# SCHEMA 1: PROPERTIES
# TABLE: QUEUE_DETAILS
# --------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS PROPERTIES_QUEUE_DETAILS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    INPUT_QUEUE TEXT,
    COPY_QUEUE TEXT,
    ERROR_QUEUE TEXT,
    BUSINESS_ERROR_QUEUE TEXT,
    OUTPUT_QUEUE TEXT,
    PROCESS_ID TEXT,
    CATEGORY TEXT,
    PAP TEXT,
    UNIQUE (PROCESS_ID, CATEGORY)
)
''')

# --------------------------------------
# SCHEMA 2: ROUTING
# TABLE: ROUTING_ENTRIES (Empty for now)
# --------------------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS ROUTING_ROUTING_ENTRIES (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    SOURCE TEXT,
    DESTINATION TEXT,
    ROUTE_TYPE TEXT
    -- Add columns as needed later
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print(f"Database '{db_name}' created with two logical schemas: 'PROPERTIES' and 'ROUTING'.")