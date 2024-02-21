import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("sm_app.sqlite")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

create_users_table = """
CREATE TABLE IF NOT EXISTS image_measurements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT NOT NULL,
  thorax_x INTEGER,
  thorax_y INTEGER,
  heart_x INTEGER,
  heart_y INTEGER
);
"""
execute_query(connection, create_users_table)

create_users = """
INSERT INTO
  image_measurements (filename, thorax_x, thorax_y, heart_x, heart_y)
VALUES
  ('img000001', 100, 100, 500, 100);
"""

execute_query(connection, create_users)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

select_users = "SELECT * from image_measurements"
users = execute_read_query(connection, select_users)

for user in users:
    print(user)

update_post_description = """
UPDATE
  image_measurements
SET
  thorax_x = 100,
  thorax_y = 300,
  heart_x = 500,
  heart_y = 300
WHERE
  filename = 'img000001'
"""

execute_query(connection, update_post_description)

post_description = execute_read_query(connection, update_post_description)

for description in post_description:
    print(description)




