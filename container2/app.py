from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta, timezone

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkin_time TEXT NOT NULL,
            checkout_time TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route("/checkin", methods=["POST"])
def checkin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM checkins WHERE checkout_time IS NULL ORDER BY id DESC LIMIT 1"
    )
    checkin = cursor.fetchone()
    if checkin:
        return "You are already checked in. Please check out first."
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO checkins (checkin_time) VALUES (?)", (current_time,)
        )
        conn.commit()
        conn.close()
        return "Checked in successfully"


@app.route("/checkout", methods=["POST"])
def checkout():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM checkins WHERE checkout_time IS NULL ORDER BY id DESC LIMIT 1"
    )
    checkin = cursor.fetchone()
    if checkin:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE checkins SET checkout_time = ? WHERE id = ?",
            (current_time, checkin["id"]),
        )
        conn.commit()
        conn.close()
        return "Checked out successfully"
    else:
        return "You have not checked in yet!"


def convert_to_moscow_time(timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    utc_time = dt.replace(tzinfo=timezone.utc)

    msk_offset = timedelta(hours=3)

    msk_time = utc_time + msk_offset

    msk_time_str = msk_time.strftime("%Y-%m-%d %H:%M:%S %Z")

    return msk_time_str


@app.route("/last_checkins")
def last_checkins():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM checkins ORDER BY id DESC LIMIT 10")
    checkins = cursor.fetchall()
    conn.close()

    checkins_list = []
    for index, row in enumerate(checkins[::-1]):
        checkin_time = convert_to_moscow_time(row["checkin_time"])
        checkout_time = (
            convert_to_moscow_time(row["checkout_time"])
            if row["checkout_time"]
            else None
        )
        if checkout_time:
            checkins_list.append(
                f"{index+1}. Check-in Time: {checkin_time} -- Check-out Time: {checkout_time}"
            )
        else:
            checkins_list.append(
                f"{index+1}. Check-in Time: {checkin_time} -- Not checked out"
            )

    return "\n".join(checkins_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
