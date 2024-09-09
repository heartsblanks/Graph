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

        @self.app.route('/graph/<value>', methods=['GET'])
        def graph(value):
            query1 = '''
        SELECT DISTINCT 
            SUBSTR(D, 
                INSTR(D, '_', INSTR(D, '_') + 1) + 1, 
                INSTR(D, '_', INSTR(D, '_', INSTR(D, '_') + 1) + 1) - INSTR(D, '_', INSTR(D, '_') + 1) - 1
            ) AS destination
        FROM table1
        WHERE A = ? AND D LIKE '%_%_%_%'
    '''
    
    query2 = '''
        SELECT DISTINCT 
            SUBSTR(D, 
                INSTR(D, '_', INSTR(D, '_') + 1) + 1, 
                INSTR(D, '_', INSTR(D, '_', INSTR(D, '_') + 1) + 1) - INSTR(D, '_', INSTR(D, '_') + 1) - 1
            ) AS destination
        FROM table2
        WHERE A = ? AND D LIKE '%_%_%_%'
    '''
data1 = self.db_manager.query_database(query1, (value,))
            data2 = self.db_manager.query_database(query2, (value,))

            combined_data = {
                'parent': value,
                'children': {
                    'table1': [d[0] for d in data1],
                    'table2': [d[0] for d in data2]
                }
            }

            # Create and generate Plotly graph
            G = self.graph_visualizer.create_graph(value, combined_data['children'])
            graph_html = self.graph_visualizer.generate_plotly_graph(G)

            return render_template('graph.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
