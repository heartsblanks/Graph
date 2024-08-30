from flask import Flask, render_template, request, jsonify

class FlaskApp:
    def __init__(self, db_manager):
        self.app = Flask(__name__)
        self.db_manager = db_manager

        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/get_data', methods=['POST'])
        def get_data():
            column_value = request.json.get('column_value')
            # Example query: Adjust this to match your actual schema
            query = 'SELECT * FROM table1 WHERE A = ?'
            results = self.db_manager.query_database(query, (column_value,))
            return jsonify(results)

        @self.app.route('/graph', methods=['POST'])
        def graph():
            column_value = request.json.get('column_value')
            # Fetch data from both tables for the selected column value
            query1 = 'SELECT D FROM table1 WHERE A = ?'
            query2 = 'SELECT D FROM table2 WHERE A = ?'
            data1 = self.db_manager.query_database(query1, (column_value,))
            data2 = self.db_manager.query_database(query2, (column_value,))

            # Combine the data for visualization (adjust as needed)
            combined_data = {
                'table1': [d[0] for d in data1],
                'table2': [d[0] for d in data2]
            }
            return jsonify(combined_data)

    def run(self, debug=True):
        self.app.run(debug=debug)