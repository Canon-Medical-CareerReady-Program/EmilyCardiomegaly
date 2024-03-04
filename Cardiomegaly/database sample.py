import sqlite3
import os
from sqlite3 import Error
from database import Database

os.remove("sm_app.sqlite")

database = Database("sm_app.sqlite")

create_results_table_sql = """
CREATE TABLE IF NOT EXISTS results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename TEXT NOT NULL,
  thorax_x INTEGER,
  thorax_y INTEGER,
  heart_x INTEGER,
  heart_y INTEGER
);
"""
database.execute_query(create_results_table_sql)

## What is this doing?
create_results_sql = """
INSERT INTO
  results (filename, thorax_x, thorax_y, heart_x, heart_y)
VALUES
  ('img000001', 100, 100, 500, 100);
"""
database.execute_query(create_results_sql)


## What is this doing?
select_results_sql = "SELECT * from results"
results = database.execute_read_query(select_results_sql)
for user in results:
    print(user)
first_image = results[0][1]
print(f"First image name is: {first_image}")

## What is this doing?
update_result_sql = f"""
UPDATE
  results
SET
  thorax_x = 100, thorax_y = 300, heart_x = 500, heart_y = 300
WHERE
  filename = '{first_image}'
"""
database.execute_query(update_result_sql)

## What is this doing?
updated_results = database.execute_read_query(select_results_sql)
for result in updated_results:
    print(result)

## What is this doing?
print(f" thorax_y for {first_image} was previously {results[0][3]} and now is {updated_results[0][3]}")



