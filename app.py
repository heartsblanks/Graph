from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to query the database based on user selection
def query_db(selected_value):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Query both tables to get values from Column D where Column A matches the selected value
    cursor.execute("SELECT D FROM table1 WHERE A=?", (selected_value,))
    column_d_values_table1 = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT D FROM table2 WHERE A=?", (selected_value,))
    column_d_values_table2 = [row[0] for row in cursor.fetchall()]

    conn.close()

    # Combine results from both tables
    combined_values = column_d_values_table1 + column_d_values_table2
    return combined_values

@app.route('/')
def index():
    return render_template('index.html', unique_values=unique_values_column_a)

@app.route('/get_data', methods=['POST'])
def get_data():
    selected_value = request.form['selected_value']
    combined_values = query_db(selected_value)
    
    return render_template('graph.html', combined_values=combined_values, selected_value=selected_value)

if __name__ == '__main__':
    app.run(debug=True)