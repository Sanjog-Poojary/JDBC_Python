import sqlite3
import os

paths = [
    os.path.join(os.path.dirname(__file__), 'drugstore.db'),
    os.path.join(os.path.dirname(__file__), '..', 'instance', 'drugstore.db'),
    os.path.join(os.path.dirname(__file__), 'instance', 'drugstore.db'),
    os.path.join(os.path.dirname(__file__), '..', 'drugstore.db'),
]

for p in paths:
    p = os.path.abspath(p)
    print('\nDB:', p)
    if os.path.exists(p):
        try:
            con = sqlite3.connect(p)
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            rows = cur.fetchall()
            print('Tables:', rows)
            con.close()
        except Exception as e:
            print('Error:', e)
    else:
        print('Missing')
