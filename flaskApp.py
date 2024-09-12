from flask import Flask, render_template, jsonify
from database_manager import DatabaseManager

class FlaskApp:
    def __init__(self, db_manager):
        self.app = Flask(__name__)
        self.db_manager = db_manager

        @self.app.route('/')
        def index():
            query = 'SELECT DISTINCT A FROM table1 UNION SELECT DISTINCT A FROM table2'
            unique_values = self.db_manager.query_database(query)
            unique_values = [item[0] for item in unique_values]
            return render_template('index.html', unique_values=unique_values)

        @self.app.route('/data')
        def data():
            coordinates = self.db_manager.get_coordinates()
            return jsonify(coordinates)

        @self.app.route('/graph/<value>', methods=['GET'])
        def graph(value):
            query1 = 'SELECT D, F, G FROM table1 WHERE A = ?'
            query2 = 'SELECT D, F, G FROM table2 WHERE A = ?'
            data1 = self.db_manager.query_database(query1, (value,))
            data2 = self.db_manager.query_database(query2, (value,))

            # Combine data from both tables
            links = []
            destinations = []

            for d in data1 + data2:
                dest, f_data, g_data = d
                if dest not in destinations:
                    destinations.append(dest)

                # Add to links with f_data and g_data for display on the link
                links.append({
                    'source': value,
                    'target': dest,
                    'f_data': f_data,
                    'g_data': g_data
                })

            # Remove duplicates and prepare graph data
            destinations = list(set(destinations))

            nodes = [{'id': value, 'group': 1}]  # The source node
            for dest in destinations:
                nodes.append({'id': dest, 'group': 2})  # Destination nodes

            graph_data = {'nodes': nodes, 'links': links}
            return jsonify(graph_data)