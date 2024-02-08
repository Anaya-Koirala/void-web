import sqlite3
import datetime

today = datetime.datetime.now()
today = today.strftime("%d-%b-%y")


def create_conn():
    return sqlite3.connect("shitposts.db")


def create_table():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS shitposts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(15) NOT NULL,
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
    cursor.execute("SELECT * FROM shitposts ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data


def create_shitpost(username, content):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO shitposts (username, date, content) VALUES (?, ?, ?)",
        (username, today, content),
    )

    conn.commit()
    conn.close()


def delete_shitpost(post_id):
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM shitposts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()
