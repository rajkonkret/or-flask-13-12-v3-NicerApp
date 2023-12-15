import sqlite3
import os

print(os.urandom(60))
try:
    sql_connection = sqlite3.connect('data/cantor.db')
    cursor = sql_connection.cursor()
    query = '''create table transactions(id integer primary key autoincrement, currency varchar(5), amount int, user varchar(5), trans_date date not null default(date()));
    '''
    add_users_query = '''CREATE TABLE users(
    id integer primary key autoincrement,
    name varchar(100) not null unique,
    email varchar(100) not null unique,
    password text,
    is_active boolean not null default 0,
    is_admin boolean not null default 0
    );'''
    # cursor.execute(query)
    cursor.execute(add_users_query)
    sql_connection.commit()
except Exception as e:
    print("Bład", e)
finally:
    if sql_connection:
        sql_connection.close()
