import sqlite3
from fastapi import FastAPI, Path, UploadFile, File, Form
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import stripe
import requests
import os
from PIL import Image
import shutil

app = FastAPI()
Base = declarative_base()
engine = create_engine('sqlite:///db.sqlite3')

class Stats(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
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
    items = Stats(name=name, description=description)
    db.add(items)
    db.commit()

    return {'message': 'Повідомленння створено'}

@app.get("/items")
def get_items(name: str = str, description: str = str, contact = str, limit : int = 50):
    db = SessionLocal()
    items = db.query(Stats).all()
    db.commit()
    return [{'item_id': i.items_id, 'name': i.name, 'description': i.description, 'contact': i.contact}
            for i in items]

@app.get("/items/{item_id}")
def get_item(item_id: int = Path(...), limit: int = 10, offset: int = 0):
    db = SessionLocal()
    item = db.query(Stats).filter(item_id == item_id).first()
    if item:
        return {'item_id': item.item_id, 'name': item.name, 'description': item.description}
    else:
        return {'error':'not found'}
@app.post("/upload/found")
def upload_found(file: UploadFile = File(...),
        lat: float = Form(...),
        lon: float = Form(...),
        contact: str = Form(...)
):
    print("Запускаємо відповідний пайплайн")
    return handle_upload(file, lat, lon, contact, status='found')
@app.post("/upload/lost")
def upload_lost(
        file: UploadFile = File(...),
        lat: float = Form(...),
        lon: float = Form(...),
        contact: str = Form(...)
):
        print("Запускаємо пайплайн для пошуку тварини")
        return handle_upload(file, lat, lon, contact, status = 'lost')

def handle_upload(file, id, lat, lon, contact, status):
    file_path = os.path.join('photos', file.filename)
    with open(file_path, 'wb') as file:
        file.write(file.read())
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE animals SET status = ? WHERE id = ?", (status, id))
    conn.commit()
    conn.close()

@app.get('/geodata')
def get_geodata(lat: float, lon: float, limit: int = 30):
    db = SessionLocal()
    geodata = ';'.join([str(lat), str(lon)])

@app.post('/geodata')

@app.delete("/items/{item_id}")
def delete_item(item_id: int = Path(...), limit: int = 5, offset: int = 0):
    db = SessionLocal()
    item = db.query(Stats).filter(item_id == item_id).first()
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

images = [f for f in os.listdir('photos') if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
os.mkdir('./saved_images')
size_limit = 200 * 1024 * 1024
def img_sorter(id, confidence_score):
    for file_name in os.listdir('./photos'):
        file_path = os.path.join('photos', file_name)
        file_size = os.path.getsize(file_path)
        if file_size <= size_limit and confidence_score >= 0.8:
            shutil.move(file_path, os.listdir('./saved_images')[0])
    return os.listdir('./saved_images')