import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Отримуємо шлях до папки, де лежить цей файл (тобто до папки src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# База завжди буде лежати в project_bobik/src/db.sqlite3
DB_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)