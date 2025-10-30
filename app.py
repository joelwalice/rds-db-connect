from flask import Flask, render_template, request
import pymysql
from os import environ as env
import os
from dotenv import load_dotenv

load_dotenv("/opt/flaskapp/.env")

app = Flask(__name__)

def get_db_connection():
    try:
        conn = pymysql.connect(
            host=env["DB_HOST"],
            user=env["DB_USER"],
            password=env["DB_PASSWORD"],
            database=env["DB_NAME"],
            port=int(env["DB_PORT"])
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

@app.route('/')
def index(): 
    conn = get_db_connection()
    if conn:
        db_status = "Database Connected Successfully!"
        print("Database connection established.")
        conn.close()
    else:
        db_status = "Database Connection Failed!"
    return render_template('index.html', db_status=db_status)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS feedbacks (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), feedback TEXT)"
        )
        cursor.execute(
            "INSERT INTO feedbacks (name, email, feedback) VALUES (%s, %s, %s)",
            (name, email, feedback)
        )
        conn.commit()
        conn.close()
        return render_template('success.html', name=name)
    else:
        return "Database connection error!", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
