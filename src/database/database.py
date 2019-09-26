import sqlite3
import socket

def create_db():
    filename = "data/" + socket.gethostname() + ".db"
    db_file = open(filename, "w")
    db_file.close()

def connect_to_db():
    return sqlite3.connect("data/" + socket.gethostname() + ".db")

def create_table(database, cursor, _name):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS {0} (
            date TIMESTAMP,
            value INTEGER    
        )
        """
        .format(_name)
    )
    database.commit()

def insert_timestamp(database, cursor, data):
    cursor.execute(
        """
        INSERT INTO {0}(date, value) VALUES (?,?)
        """
        .format(data.get_name()),
        (data.get_date(), data.get_value())
    )

    database.commit()