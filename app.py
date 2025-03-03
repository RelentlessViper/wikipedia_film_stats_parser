from flask import Flask, jsonify, render_template
import sqlite3
import json

app = Flask(__name__)

# Function to fetch data from our DB
def get_films():
    conn = sqlite3.connect('film_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM films')
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    films = []
    for row in rows:
        film = dict(zip(columns, row))
        temp_budget = film["budget"]
        temp_box_office = film["box_office"]
        
        if len(temp_budget.split()) > 1:
            temp_budget = temp_budget[1:-1].split(",")
            film["average_budget"] = (int(temp_budget[0]) + int(temp_budget[1])) / 2
        else:
            film["average_budget"] = int(temp_budget)

        if len(temp_box_office.split()) > 1:
            temp_box_office = temp_box_office[1:-1].split(",")
            film["average_box_office"] = (int(temp_box_office[0]) + int(temp_box_office[1])) / 2
        else:
            film["average_box_office"] = int(temp_box_office)

        films.append(film)
    conn.close()
    return films

# API endpoint to retrieve the data
@app.route('/api/films', methods=['GET'])
def films():
    films = get_films()
    return jsonify(films)

# API endpoint to render the HTML page
@app.route('/')
def index():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run(debug=True)