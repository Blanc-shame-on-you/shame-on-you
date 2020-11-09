import sqlite3

conn = sqlite3.connect('people.db')
cur = conn.cursor()

CREATE_sql = 'CREATE TABLE people(idx integer primary key autoincrement, appear_at datetime DEFAULT CURRENT_TIMESTAMP, img BLOB);'
conn.execute(CREATE_sql)

conn.commit()
conn.close()
