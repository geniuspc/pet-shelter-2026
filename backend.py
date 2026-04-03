import sqlite3
from fastapi import FastAPI, Path
from sqlaclhemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import stripe
import requests
import os


app = FastAPI()
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True) + 1
    name = Column(String)
    age = Column(Integer, primary_key=True)
    description = Column(String)
    path = Column(String)
    contact = Column(String)
    lang = Column(String)
    lat = Column(String)
    status = Column(String)
    matches = Column(String)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


@app.post("/items")
def create_items(name = str, description = str):
    db = SessionLocal()
    items = Item(name=name, description=description)
    db.add(items)
    db.commit()

    return {'message': 'Повідомленння створено'}

@app.get("/items")
def get_items(name: str = str, description: str = str, limit : int = 50):
    db = SessionLocal()
    items = db.query(Item).all()
    db.commit()
    return [{'item_id': i.items_id, 'name': i.name, 'description': i.description}
            for i in items]

@app.get("/items/{item_id}")
def get_item(item_id: int = Path(...), limit: int = 5, offset: int = 0):
    db = SessionLocal()
    item = db.query(Item).filter(item_id == item_id).first()
    if item:
        return {'item_id': item.item_id, 'name': item.name, 'description': item.description}
    else:
        return {'error':'not found'}

@app.delete("/items/{item_id}")
def delete_item(item_id: int = Path(...), limit: int = 5, offset: int = 0):
    db = SessionLocal()
    item = db.query(Item).filter(item_id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return {'message': 'Item deleted'}
    else:
        return {'error':'not found'}

def image_saver(url, folder_name, file_name):
    if not os.path.exists(folder_name):
        os.mkdir('photos')
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        path = os.path.join(folder_name, file_name)

        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=2048):
                file.write(chunk)
        print(f"Изображение сохранено в {path}")
