from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///db.sqlite3')
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
