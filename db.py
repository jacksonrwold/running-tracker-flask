import sqlite3

conn = sqlite3.connect("runs.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE run (
    id INTEGER PRIMARY KEY,
    time TEXT NOT NULL,
    distance DECIMAL(5,2) NOT NULL,
    calories INTEGER NOT NULL
)"""

cursor.execute(sql_query)