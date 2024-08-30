from flask import Flask, render_template, request, jsonify

class FlaskApp:
    def __init__(self, db_manager):
        self.app = Flask(__name__)
        self.db_manager = db_manager

        @self.app.route('/')
        def index():
            # Query to get all unique values from column A
            query = 'SELECT DISTINCT A FROM table1 UNION SELECT DISTINCT A FROM table2'
            unique_values = self.db_manager.query_database(query)
            # Flatten the list of tuples into a single list
            unique_values = [item[0] for item in unique_values]
            return render_template('index.html', unique_values=unique_values)

        @self.app.route('/graph/<value>', methods=['GET'])
        def graph(value):
            # Fetch data from both tables for the selected column value
            query1 = 'SELECT D FROM table1 WHERE A = ?'
            query2 = 'SELECT D FROM table2 WHERE A = ?'
            data1 = self.db_manager.query_database(query1, (value,))
            data2 = self.db_manager.query_database(query2, (value,))

            # Combine the data for visualization
            combined_data = {
                'table1': [d[0] for d in data1],
                'table2': [d[0] for d in data2]
            }

            # Pass the data to the template for rendering the graph
            return render_template('graph.html', value=value, data=combined_data)

    def run(self, debug=True):
        self.app.run(debug=debug)