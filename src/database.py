import sqlite3
import os
from datetime import datetime, date
import logging

# データベースファイルのパスを設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")


# Function to create the database file if it does not exist
def create_database():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            # Example of table creation (modify as needed)
            c.execute(
                """
                CREATE TABLE performances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    duration INTEGER NOT NULL
                )
            """
            )
            conn.commit()
        print(f"Database created at {DB_PATH}")


print(f"Database path: {DB_PATH}")  # デバッグ情報

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS performances 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              start_time TEXT, 
              end_time TEXT, 
              total_duration REAL)"""
)
conn.commit()


def insert_start_time(start_time):
    start_datetime = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
    # 既存の未終了レコードがない場合のみ新しいレコードを挿入
    c.execute("SELECT * FROM performances WHERE end_time IS NULL")
    if c.fetchone() is None:
        c.execute(
            "INSERT INTO performances (start_time, end_time, total_duration) VALUES (?, ?, ?)",
            (start_datetime, None, 0),
        )
        conn.commit()
    # logging.info(f"Inserted start time: {start_datetime}")  # デバッグ情報


def update_total_duration(total_time):
    # logging.info("Updating total duration")  # デバッグ情報
    c.execute(
        "UPDATE performances SET total_duration = total_duration + ? WHERE end_time IS NULL",
        (total_time,),
    )
    conn.commit()


def update_end_time():
    # logging.info("Updating end time")  # デバッグ情報
    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "UPDATE performances SET end_time = ? WHERE end_time IS NULL", (end_datetime,)
    )
    conn.commit()
    # logging.info(f"Updated end time: {end_datetime}")  # デバッグ情報


def calculate_today_durations():
    # logging.info("Calculating today's durations")  # デバッグ情報
    start_duration = 0
    total_duration = 0
    today = date.today().strftime("%Y-%m-%d")

    performances = c.execute(
        "SELECT * FROM performances WHERE DATE(start_time) = ?", (today,)
    ).fetchall()
    # logging.info(f"Performances: {performances}")  # デバッグ情報
    for performance in performances:
        start_time = datetime.strptime(performance[1], "%Y-%m-%d %H:%M:%S")
        if performance[2]:
            end_time = datetime.strptime(performance[2], "%Y-%m-%d %H:%M:%S")
            start_duration += (end_time - start_time).total_seconds()
        total_duration += performance[3]

    return start_duration, total_duration


def fetch_latest_performances():
    # logging.info("Fetching latest performances")  # デバッグ情報
    today = date.today().strftime("%Y-%m-%d")
    performances = c.execute(
        "SELECT * FROM performances ORDER BY start_time DESC LIMIT 10"
    ).fetchall()
    # logging.info(f"Fetched performances: {performances}")  # デバッグ情報
    return performances
