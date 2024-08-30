from flask import Flask, render_template, jsonify
from database_manager import DatabaseManager

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
            # Return data for hexbin map
            coordinates = self.db_manager.get_coordinates()
            return jsonify(coordinates)