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

        @app.route('/graph/<value>', methods=['GET'])
def graph(value):
    query1 = 'SELECT D, F, G FROM table1 WHERE A = ?'
    query2 = 'SELECT D, F, G FROM table2 WHERE A = ?'
    data1 = self.db_manager.query_database(query1, (value,))
    data2 = self.db_manager.query_database(query2, (value,))

    # Combine data from both tables
    destinations = data1 + data2  # This will contain D, F, and G now

    nodes = [{'id': value, 'group': 1}]  # The source node
    links = []

    for dest in destinations:
        destination, column_f, column_g = dest[0], dest[1], dest[2]
        if destination not in [node['id'] for node in nodes]:
            nodes.append({'id': destination, 'group': 2})  # Destination nodes
        links.append({
            'source': value, 
            'target': destination, 
            'f_data': column_f,  # Add F data
            'g_data': column_g   # Add G data
        })

    graph_data = {'nodes': nodes, 'links': links}
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)
