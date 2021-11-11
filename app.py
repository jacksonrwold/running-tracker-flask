from flask import Flask, request, jsonify
import json
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"/runs": {"origins": "*"}, r"/run/*": {"origins": "*"}})

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('runs.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/runs", methods=['GET', 'POST'])
def runs():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM run")
        runs = [
            dict(id=row[0], time=row[1], distance=row[2], calories=row[3])
            for row in cursor.fetchall()
        ]
        if runs is not None:
            return jsonify(runs)
    
    if request.method == 'POST':
        json = request.get_json()
        new_time = json['time']
        new_distance = json['distance']
        new_calories = json['calories']

        sql = """ INSERT INTO run (time, distance, calories)
                  VALUES (?, ?, ?)      """

        cursor = cursor.execute(sql, (new_time, new_distance, new_calories))
        conn.commit()

        return f"Run with the id of: {cursor.lastrowid} created successfully"

@app.route("/run/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_run(id):
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute(""" SELECT * FROM run WHERE id=? """, (id,))
        
        checkIfValid = cursor.fetchall()
        for x in checkIfValid:
            checkIfValid = x
        if checkIfValid is not None:
            run = [
                dict(id=checkIfValid[0], time=checkIfValid[1], distance=checkIfValid[2], calories=checkIfValid[3])
            ]
            return jsonify(run), 200
        else:
            return "Run with that ID does not exist", 404
    
    if request.method == 'PUT':
        sql = """ UPDATE run
                SET time = ?,
                    distance = ?,
                    calories = ?
                WHERE id=? """

        json = request.get_json()
        new_time = json['time']
        new_distance = json['distance']
        new_calories = json['calories']

        updated_run = {
            'id': id,
            'time': new_time,
            'distance': new_distance,
            'calories': new_calories
        }

        conn.execute(sql, (new_time, new_distance, new_calories, id))
        conn.commit()

        return jsonify(updated_run)
    if request.method == 'DELETE':
        sql = """ DELETE FROM run WHERE id=? """

        conn.execute(sql, (id,))
        conn.commit()

        return f"Run with ID: {id} was deleted", 200
            


if __name__ == '__main__':
    app.run(debug=True)
