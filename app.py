from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import random

app = Flask(__name__)
CORS(app)

# Connect to your MySQL DB
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Clever@101",
    database="its_math"
)

# ✅ Serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Serve year pages
@app.route('/year<int:year>')
def year_page(year):
    return render_template(f'year{year}.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/startlearning')
def start_learning():
    return render_template('startlearning.html')

@app.route('/thankyou')
def thankyou():
    print("✅ /thankyou route was hit!")
    return render_template('thankyou.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    year = request.args.get('year', type=int)
    topic = request.args.get('topic')
    difficulty = request.args.get('difficulty')

    cursor = db.cursor(dictionary=True)

    if year and topic:
        cursor.execute("""
            SELECT * FROM questions 
            WHERE year = %s AND topic = %s AND difficulty = %s 
            ORDER BY RAND() LIMIT 1
        """, (year, topic, difficulty))
    elif year:
        cursor.execute("""
            SELECT * FROM questions 
            WHERE year = %s AND difficulty = %s 
            ORDER BY RAND() LIMIT 1
        """, (year, difficulty))
    elif difficulty:
        cursor.execute("""
            SELECT * FROM questions 
            WHERE difficulty = %s 
            ORDER BY RAND() LIMIT 1
        """, (difficulty,))
    else:
        cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 1")

    question = cursor.fetchone()
    return jsonify(question)


if __name__ == '__main__':
    app.run(debug=True)

