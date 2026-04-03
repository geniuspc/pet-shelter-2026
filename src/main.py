from fastapi import FastAPI, UploadFile, File, Form, Path
import os
import requests
import shutil
from database import SessionLocal, engine, Base
from model import Dog
os.makedirs('photos', exist_ok=True)
os.makedirs('saved_images', exist_ok=True)

app = FastAPI()
os.makedirs("../photos", exist_ok=True)
Base.metadata.create_all(engine)
@app.post("/items")
def create_items(name: str, description: str):
    db = SessionLocal()

    item = Dog(name=name, description=description)

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"id": item.id}

@app.post("/upload/lost")
def upload_lost(
    file: UploadFile = File(...),
    lat: float = Form(...),
    lon: float = Form(...),
    contact: str = Form(...)
):
    return handle_upload(file, lat, lon, contact, "lost")

@app.post("/upload/found")
def upload_found(
    file: UploadFile = File(...),
    lat: float = Form(...),
    lon: float = Form(...),
    contact: str = Form(...)
):
    return handle_upload(file, lat, lon, contact, "found")

def handle_upload(file, lat, lon, contact, status, age, gender):
    db = SessionLocal()

    file_path = os.path.join("../photos", file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    dog = Dog(
        path=file_path,
        contact=contact,
        status=status,
        age=age,
        gender=gender
    )

    db.add(dog)
    db.commit()
    db.refresh(dog)

    return {"id": dog.id}

@app.get("/items")
def get_items():
    db = SessionLocal()

    items = db.query(Dog).all()

    return [
        {"id": i.id, "path": i.path, "status": i.status}
        for i in items
    ]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    db = SessionLocal()
    item = db.query(Dog).filter(Dog.id == item_id).first()
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