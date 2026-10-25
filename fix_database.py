import sqlite3
from pathlib import Path

db_path = Path("instance/zero_waste.db")

if not db_path.exists():
    print("Database file not found:", db_path)
    raise SystemExit(1)

con = sqlite3.connect(db_path)

try:
    columns = [
        row[1]
        for row in con.execute("PRAGMA table_info(food)").fetchall()
    ]

    if not columns:
        print("Food table not found in zero_waste.db")
    elif "cost_type" in columns:
        print("cost_type already exists. No change needed.")
    else:
        con.execute(
            "ALTER TABLE food ADD COLUMN cost_type "
            "VARCHAR(50) NOT NULL DEFAULT 'Free'"
        )
        con.commit()
        print("cost_type column added successfully.")

finally:
    con.close()
