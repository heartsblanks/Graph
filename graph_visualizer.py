class GraphVisualizer:
    def __init__(self):
        pass

    def create_graph(self, parent, children_data):
        """
        Creates a network graph with the parent node and children nodes.
        """
        G = nx.Graph()
        G.add_node(parent)
        
        for child in children_data['table1']:
            G.add_node(child)
            G.add_edge(parent, child)
        
        for child in children_data['table2']:
            G.add_node(child)
            G.add_edge(parent, child)
        
        return G

    def generate_plotly_graph(self, G):
        """
        Generates a Plotly graph from a NetworkX graph.
        """
        pos = nx.spring_layout(G, seed=42)  # Use a fixed seed for consistent layout

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_y.append(y0)
            edge_y.append(y1)

        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_text = list(G.nodes())

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=2, color='black')))

        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text,
                                 textposition='bottom center', marker=dict(size=20, color='blue')))  # Increased marker size

        fig.update_layout(title='Network Graph', showlegend=False,
                          xaxis=dict(showgrid=False, zeroline=False),
                          yaxis=dict(showgrid=False, zeroline=False),
                          width=1000,  # Increase width as needed
                          height=800)  # Increase height as needed

        return fig.to_html(full_html=False)