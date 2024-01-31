import sqlite3
import datetime

today = datetime.datetime.now()
today = today.strftime("%d-%b-%y")

def create_conn():
    return sqlite3.connect("writings.db")


def create_table():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS writings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subtitle TEXT NOT NULL,
            date DATE NOT NULL,
            content TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def get_all():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM writings")
    data = cursor.fetchall()
    conn.close()
    return data


def create_writing(title, subtitle, content):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO writings (title,subtitle,date, content) VALUES (?, ?, ?, ?)",
            (title, subtitle, today, content),
    )
    conn.commit()
    conn.close()


def get_writing(post_id):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM writings WHERE id=?",
        (post_id,),
    )
    data = cursor.fetchone()
    conn.close()
    return data
