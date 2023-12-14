import sqlite3

try:
    sql_connection = sqlite3.connect('cantor_2.db')
except Exception as e:
    print("Bład", e)
finally:
    if sql_connection:
        sql_connection.close()
