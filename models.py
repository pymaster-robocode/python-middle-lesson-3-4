from database import get_db

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            owner TEXT
        )
    ''')
    conn.commit()
    conn.close()
