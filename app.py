from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

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
        new_time = request.form['time']
        new_distance = request.form['distance']
        new_calories = request.form['calories']

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
            return jsonify(checkIfValid), 200
        else:
            return "Run with that ID does not exist", 404

        return jsonify(cursor.fetchall()), 200
    
    if request.method == 'PUT':
        sql = """ UPDATE run
                SET time = ?
                    distance = ?
                    calories = ?
                WHERE id=? """

        time = request.form['time']
        distance = request.form['distance']
        calories = request.form['calories']

        updated_run = {
            'id': id,
            'time': time,
            'distance': distance,
            'calories': calories
        }

        conn.execute(sql, (time, distance, calories, id))
        conn.commit()

        return jsonify(updated_run)
    if request.method == 'DELETE':
        sql = """ DELETE FROM run WHERE id=? """

        conn.execute(sql, (id,))
            


if __name__ == '__main__':
    app.run(debug=True)