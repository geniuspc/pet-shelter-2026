import streamlit as st
from streamlit_folium import st_folium
# Якщо utils.py лежить у головній папці, імпорт залишаємо так. Якщо в views - змінимо шлях.
from utils import create_pet_map 
import os

from src.database import SessionLocal # Підключення до БД напряму
from src.model import Animal, Location # Використовуємо нові моделі

st.set_page_config(page_title="Знайшов собаку", page_icon="🐕")

if st.button("⬅️ Назад"):
    st.switch_page("views/home.py")

st.subheader("📍 Де ви бачили собаку?")

# Відмальовуємо карту
found_map = create_pet_map()
map_data = st_folium(found_map, width=700, height=400, key="found_map")

# Координати за замовчуванням (Дніпро)
clicked_lat, clicked_lon = 48.4647, 35.0461

if map_data and map_data.get("last_clicked"):
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    st.success(f"Обрано координати: {clicked_lat:.4f}, {clicked_lon:.4f}")

with st.form("found_form"):
    name = st.text_input("Ім'я (якщо відомо)")
    gender = st.selectbox("Стать", ["Хлопчик", "Дівчинка", "Невідомо"]) # Додали поле з БД
    age = st.number_input("Приблизний вік", 0, 20, 1)
    desc = st.text_area("Прикмети")
    contact = st.text_input("Ваш контакт* (обов'язково)")
    
    # Виводимо координати в форму, щоб можна було відредагувати руками
    lat_input = st.text_input("Широта", value=str(clicked_lat))
    lon_input = st.text_input("Довгота", value=str(clicked_lon))
    
    photo = st.file_uploader("Фото* (обов'язково)", type=["jpg", "png", "jpeg"])
    
    submit = st.form_submit_button("📢 Відправити")

    if submit:
        if photo and contact:
            os.makedirs("photos", exist_ok=True)
            file_path = f"photos/{photo.name}"
            with open(file_path, "wb") as f:
                f.write(photo.getbuffer())

            # 2. Робота з базою даних
            db = SessionLocal() # Відкриваємо сесію
            
            try:
                # Об'єднуємо ім'я та опис, бо в базі є тільки description
                full_desc = f"Ім'я: {name}. {desc}" if name else desc
                
                new_animal = Animal(
                name=name,
                path=file_path,
                age=age,
                gender=gender,
                status="found",
                contact=contact,
                description=desc
        )
                db.add(new_animal)
                db.commit()
                db.refresh(new_animal) # Оновлюємо, щоб отримати ID створеної тварини
                
                # Записуємо координати в таблицю locations
                new_location = Location(
                    dog_id=new_animal.id,
                    lat=str(lat_input),
                    lon=str(lon_input)
                )
                db.add(new_location)
                db.commit()
                
                st.balloons()
                st.success("Готово! Тваринку та її локацію успішно додано до бази.")
                
            except Exception as e:
                db.rollback() # Якщо помилка - скасовуємо запис
                st.error(f"Помилка при збереженні: {e}")
            finally:
                db.close() # Закриваємо з'єднання
        else:
            st.error("Будь ласка, завантажте фото та вкажіть ваш контакт!")