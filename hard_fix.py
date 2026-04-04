import sqlite3
import os

# Вказуємо шлях ТОЧНО в папку src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'src', 'db.sqlite3')

print(f"Створюємо нову базу за адресою: {db_path}")

# Якщо файл випадково залишився - видаляємо його перед створенням
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Створюємо таблицю animals з колонкою name
cursor.execute('''
CREATE TABLE animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    path TEXT,
    age INTEGER,
    gender TEXT,
    status TEXT,
    contact TEXT,
    description TEXT
)
''')

# Додаємо локації
cursor.execute('''
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dog_id INTEGER,
    lat TEXT,
    lon TEXT
)
''')

conn.commit()
conn.close()
print("✅ ПЕРЕМОГА! База створена з нуля з усіма колонками.")