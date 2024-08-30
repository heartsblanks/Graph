if __name__ == '__main__':
    # Step 1: Clean the CSV files
    cleaner = CSVCleaner()
    columns_table1 = cleaner.clean_csv('table1.csv', 'cleaned_table1.csv')
    columns_table2 = cleaner.clean_csv('table2.csv', 'cleaned_table2.csv')

    # Step 2: Create the database and load data
    db_manager = DatabaseManager()
    db_manager.create_database_and_load_data('cleaned_table1.csv', 'cleaned_table2.csv', columns_table1, columns_table2)

    # Step 3: Start the Flask application
    app = FlaskApp(db_manager)
    app.run()