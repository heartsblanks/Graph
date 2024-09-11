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
            destinations = data1 + data2  # This will contain D, F, and G now

            # Function to extract substring between the 2nd and 3rd underscores
            def extract_between_underscores(destination):
                if isinstance(destination, str):
                    parts = destination.split('_')
                    if len(parts) >= 4:
                        return parts[2]  # The part between the 2nd and 3rd underscores
                return None

            # Process destinations to extract the part between 2nd and 3rd underscores
            processed_destinations = [
                (extract_between_underscores(dest[0]), dest[1], dest[2])  # dest[0] is D, dest[1] is F, dest[2] is G
                for dest in destinations if extract_between_underscores(dest[0])
            ]
            processed_destinations = list(set(processed_destinations))  # Remove duplicates

            # Prepare graph data
            nodes = [{'id': value, 'group': 1}]  # The source node
            links = []

            # Add destination nodes and links with F-G data
            for dest, column_f, column_g in processed_destinations:
                if dest not in [node['id'] for node in nodes]:
                    nodes.append({'id': dest, 'group': 2})  # Destination nodes
                links.append({
                    'source': value, 
                    'target': dest, 
                    'f_data': column_f,  # F data
                    'g_data': column_g   # G data
                })

            graph_data = {'nodes': nodes, 'links': links}
            
            return jsonify(graph_data)  # Return the data as JSON

if __name__ == '__main__':
    app.run(debug=True)
