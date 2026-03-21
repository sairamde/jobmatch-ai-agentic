import sqlite3

conn = sqlite3.connect("candidates.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    name TEXT PRIMARY KEY,
    score INTEGER,
    strengths TEXT,
    gaps TEXT,
    url TEXT
)
""")
conn.commit()


def db_tool(action, name=None, score=None, strengths=None, gaps=None, url=None):

    if action == "INSERT":
        cursor.execute("SELECT * FROM candidates WHERE name=?", (name,))
        if cursor.fetchone():
            cursor.execute("""
            UPDATE candidates SET score=?, strengths=?, gaps=?, url=? WHERE name=?
            """, (score, strengths, gaps, url, name))
            conn.commit()
            return "Updated existing record"
        else:
            cursor.execute("INSERT INTO candidates VALUES (?, ?, ?, ?, ?)",
                           (name, score, strengths, gaps, url))
            conn.commit()
            return "Saved successfully"

    elif action == "LIST":
        cursor.execute("SELECT name, score FROM candidates")
        data = cursor.fetchall()
        return data if data else "No candidates in the database yet"

    elif action == "TOP":
        cursor.execute("SELECT name, score FROM candidates ORDER BY score DESC LIMIT 3")
        return cursor.fetchall()

    elif action == "DELETE":
        cursor.execute("SELECT * FROM candidates WHERE name=?", (name,))
        if not cursor.fetchone():
            return "No record found for that candidate"
        cursor.execute("DELETE FROM candidates WHERE name=?", (name,))
        conn.commit()
        return "Deleted successfully"

    elif action == "CLEAR":
        cursor.execute("DELETE FROM candidates")
        conn.commit()
        return "All records deleted successfully"