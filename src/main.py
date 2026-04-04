from fastapi import FastAPI, UploadFile, File, Form, Path
import os
import requests
import shutil
from src.database import SessionLocal, engine, Base
from src.model import Animal

os.makedirs('photos', exist_ok=True)
os.makedirs('saved_images', exist_ok=True)

app = FastAPI()
os.makedirs("../photos", exist_ok=True)
@app.post("/items")
def create_items(name: str, description: str):
    db = SessionLocal()

    item = Animal(name=name, description=description)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"id": item.id}

@app.post("/upload/lost")
def upload_lost(
    name: str = Form(...),
    file: UploadFile = File(...),
    lat: float = Form(...),
    lon: float = Form(...),
    contact: str = Form(...),
    age: int = Form(None),
    gender: str = Form(None)
):
    return handle_upload(name, file, lat, lon, contact, "lost")

@app.post("/upload/found")
def upload_found(
    name: str = Form(...),
    file: UploadFile = File(...),
    lat: float = Form(...),
    lon: float = Form(...),
    contact: str = Form(...),
    age: int = Form(None),
    gender: str = Form(None)
):
    return handle_upload(name, file, lat, lon, contact, "found", age, gender)

def handle_upload(name, file, lat, lon, contact, status, age=None, gender=None):
    db = SessionLocal()

    file_path = os.path.join("photos", file.filename)
    os.makedirs("photos", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    animal = Animal(
        name=name,
        path=file_path,
        contact=contact,
        status=status,
        age=age,
        gender=gender
    )

    db.add(animal)
    db.commit()
    db.refresh(animal)

    return {"id": animal.id, "name": animal.name}

@app.get("/items")
def get_items():
    db = SessionLocal()

    items = db.query(Animal).all()

    return [
        {"id": i.id,
         "path": i.path,
         "status": i.status,
         "name": i.name,
         "lat": i.lat,
         "lon": i.lon,
         "contact": i.contact
        }
        for i in items
    ]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    db = SessionLocal()
    item = db.query(Animal).filter(Animal.id == item_id).first()
    if item:
        return {
            "id": item.id,
            "path": item.path,
            "status": item.status
        }

    return {"error": "not found"}


def image_saver(url, folder_name, file_name):
    if not os.path.exists(folder_name):
        os.mkdir('../photos')
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        path = os.path.join(folder_name, file_name)

        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=2048):
                file.write(chunk)
        print(f"Изображение сохранено в {path}")

images = [f for f in os.listdir('../photos') if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp'))]
size_limit = 200 * 1024 * 1024
def img_sorter(id, confidence_score):
    for file_name in os.listdir('../photos'):
        file_path = os.path.join('../photos', file_name)
        file_size = os.path.getsize(file_path)
        if file_size <= size_limit and confidence_score >= 0.8:
            shutil.move(file_path, os.listdir('../saved_images')[0])
    return os.listdir('../saved_images')