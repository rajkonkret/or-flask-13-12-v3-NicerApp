import sqlite3

try:
    sql_connection = sqlite3.connect('data/cantor.db')
    cursor = sql_connection.cursor()
    query = '''create table transactions(id integer primary key autoincrement, currency varchar(5), amount int, user varchar(5), trans_date date not null default(date()));
    '''
    cursor.execute(query)
    sql_connection.commit()
except Exception as e:
    print("Bład", e)
finally:
    if sql_connection:
        sql_connection.close()
