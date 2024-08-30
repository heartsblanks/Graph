from flask import Flask, render_template, jsonify
import pandas as pd
import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def query_database(self, query):
        with sqlite3.connect(self.db_name) as conn:
            return conn.execute(query).fetchall()

class FlaskApp:
    def __init__(self, db_manager):
        self.app = Flask(__name__)
        self.db_manager = db_manager

        @self.app.route('/')
        def index():
            # Query unique values from column A
            query = 'SELECT DISTINCT A FROM table1 UNION SELECT DISTINCT A FROM table2'
            unique_values = self.db_manager.query_database(query)
            unique_values = [item[0] for item in unique_values]
            return render_template('index.html', unique_values=unique_values)

        @self.app.route('/data')
        def data():
            # Return data in JSON format for hexbin map
            query = 'SELECT A FROM table1 UNION SELECT A FROM table2'
            data = self.db_manager.query_database(query)
            
            # Assign coordinates (example coordinates; adjust as needed)
            df = pd.DataFrame({'A': [item[0] for item in data]})
            df['x'] = df.index % 50 * 20  # Adjust as needed
            df['y'] = df.index // 50 * 20 # Adjust as needed
            data_json = df[['x', 'y']].to_dict(orient='records')
            
            return jsonify(data_json)

if __name__ == '__main__':
    db_manager = DatabaseManager('your_database.db')
    app = FlaskApp(db_manager)
    app.app.run(debug=True)