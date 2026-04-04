import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import time
import math

# 1. НАЛАШТУВАННЯ СТОРІНКИ ТА СТИЛІВ

st.set_page_config(
    page_title="Пошук Бобика", 
    page_icon="🐾", 
    layout="centered"
)

# Кастомний CSS 
st.markdown(""" 
    <style> 
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    .stButton>button {width: 100%; border-radius: 10px; height: 60px; font-size: 18px; font-weight: bold;} 
    .big-success { 
        font-size: 24px; 
        color: #28a745; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 20px; 
    } 
    </style>
""", unsafe_allow_html=True)

# 2. УНІВЕРСАЛЬНА ФУНКЦІЯ КАРТИ

def create_pet_map(center_lat=48.4647, center_lon=35.0461):
    """Створює карту Дніпра з радіусом пошуку 80 км"""
    
    bounds = [
       [47.70, 33.90], 
       [49.25, 36.20]
    ]
    
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=9,
        min_zoom=9,
        max_bounds=True,
        min_lat=bounds[0][0], max_lat=bounds[1][0],
        min_lon=bounds[0][1], max_lon=bounds[1][1]
        )
    
# Встановлюємо межі
    m.fit_bounds(bounds)

    # Малюємо коло 80 км (80 000 метрів)
    folium.Circle(
        radius=80000,
        location=[center_lat, center_lon],
        color="crimson",
        fill=True,
        fill_opacity=0.1,
        interactive=False,
    ).add_to(m)
    
    return m

# 3. ІНІЦІАЛІЗАЦІЯ СТАНУ СЕСІЇ

if 'page' not in st.session_state: 
    st.session_state.page = 'main'

if 'submission_success' not in st.session_state: 
    st.session_state.submission_success = False

# Макетна база даних для каталогу (у реалі буде запит до бекенду)
if 'pets_db' not in st.session_state:
    st.session_state.pets_db = [
        {"id": 0, "name": "Барон", "age": 2, "status": "Шукає дім", "desc": "Дуже добрий белік", "img": "photo/0E1A8113.jpeg"},
        {"id": 1, "name": "Альма", "age": 1, "status": "На адаптації", "desc": "Грайлива та енергійна", "img": "photo/0E1A8132.jpeg"},
        {"id": 2, "name": "Рекс", "age": 5, "status": "Шукає дім", "desc": "Надійний добряк", "img": "photo/0E1A8136.jpeg"},
         {"id": 3, "name": "Абоба", "age": 7, "status": "Шукає дім", "desc": "Енергічний пройдисвіт", "img": "photo/0E1A8159.jpeg"},
    ]

# 4. СТОРІНКА 1: ГОЛОВНА

if st.session_state.page == 'main':
    st.title("🐾 Служба порятунку Бобиків")
    st.write("Оберіть розділ:")
    
    # Робимо 3 колонки для кнопок
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🐕 Знайшов"):
            st.session_state.page = 'found'; st.rerun()
    with c2:
        if st.button("😢 Шукаю"):
            st.session_state.page = 'lost'; st.rerun()
    with c3:
        if st.button("🏠 Притулок"): # Нова кнопка
            st.session_state.page = 'catalog'; st.rerun()

    # Кнопка для бекендера (Донати) у сайдбарі
    st.sidebar.header("Підтримка")
    if st.sidebar.button("💰 Зробити донат"):
        st.sidebar.info("Тут бекендер підключить Monobank API або LiqPay")

#СТОРІНКА 2: ЗНАЙШОВ СОБАКУ

elif st.session_state.page == 'found':
    if st.button("⬅️ Назад на головну"):
        st.session_state.page = 'main'
        st.rerun()

    st.subheader("📍 Де ви бачили собаку?")
    st.info("Клікніть на карту, щоб автоматично обрати координати знахідки.")

    # Виклик функції карти
    found_map = create_pet_map()
    map_data = st_folium(found_map, width=700, height=400, key="found_map")

    # Обробка кліку по карті
    clicked_lat, clicked_lon = 48.4647, 35.0461 # Дефолт: центр Дніпра
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        st.success(f"Обрано координати: {clicked_lat:.4f}, {clicked_lon:.4f}")

    # Форма реєстрації знахідки
    if st.session_state.submission_success:
        st.markdown('<p class="big-success">🎉 Дякуємо! Ви робите добру справу! 🎉</p>', unsafe_allow_html=True)
        st.balloons()
    else:
        with st.form("found_form"):
            name = st.text_input("Ім'я (якщо відомо, або 'Невідомо')")
            age = st.number_input("Приблизний вік (років)", 0, 20, 1)
            desc = st.text_area("Прикмети (нашийник, окрас)")
            contact = st.text_input("Ваш Telegram або номер телефону")
            
            # Приховані поля для координат (беруться з карти)
            lat_input = st.text_input("Широта", value=str(clicked_lat))
            lon_input = st.text_input("Довгота", value=str(clicked_lon))
            
            photo = st.file_uploader("Фото собачки", type=["jpg", "png", "jpeg"])
            submit_found = st.form_submit_button("📢 Відправити в базу")

        if submit_found:
            if photo and contact:
                files = {"file": (photo.name, photo.getvalue(), photo.type)}
                data = {
                    "name": name, "age": age, "description": desc,
                    "lat": float(lat_input), "lon": float(lon_input), "contact": contact
                }
                try:
                    res = requests.post("http://localhost:8000/upload/found", files=files, data=data)
                    if res.status_code == 200:
                        st.session_state.submission_success = True
                        st.rerun()
                    else:
                        st.error(f"Бекенд лається: {res.text}")
                except Exception:
                    st.error("Помилка! Перевірте, чи запущений сервер Uvicorn.")
            else:
                st.warning("Додайте фото та залиште контакт для зв'язку!")

#СТОРІНКА 3: ШУКАЮ СОБАКУ

elif st.session_state.page == 'lost':
    if st.button("⬅️ Назад на головну"):
        st.session_state.page = 'main'
        st.rerun()

    st.subheader("🔍 Пошук вашого улюбленця")
    st.write("Завантажте фото, і наш ШІ знайде схожих собак у радіусі 450 км.")

    with st.form("lost_form"):
        dog_name = st.text_input("Кличка собаки")
        lost_contact = st.text_input("Ваш контакт для зв'язку")
        lost_photo = st.file_uploader("Фотографія для аналізу", type=["jpg", "png"])
        submit_lost = st.form_submit_button("🚀 Розпочати пошук")

    if submit_lost:
        if lost_photo and lost_contact:
            st.info("Аналізуємо базу оголошень...")
            time.sleep(1) # Ефект роботи ШІ
            
            st.success("Знайдено схожих собак! Перегляньте карту збігів:")
            
            # Викликаємо ту саму функцію карти для результатів
            results_map = create_pet_map()
            
            # Макетні точки для демонстрації (імітація результатів МЛ)
            points = [
                {"loc": [48.4750, 35.0600], "txt": "Збіг 95%"},
                {"loc": [48.4400, 35.0200], "txt": "Збіг 80%"}
            ]
            for p in points:
                folium.Marker(p["loc"], popup=p["txt"], icon=folium.Icon(color='green')).add_to(results_map)
            
            st_folium(results_map, width=700, height=400, key="lost_results_map")
        else:
            st.error("Завантажте фото вашого собаки для пошуку.")

            # СТОРІНКА 4: КАТАЛОГ ТВАРИН
            
elif st.session_state.page == 'catalog':
    if st.button("⬅️ На головну"):
        st.session_state.page = 'main'; st.rerun()

    st.title("🏠 Наші підопічні")
    
    # Ініціалізуємо змінну для відстеження відкритої анкети
    if 'expanded_pet_id' not in st.session_state:
        st.session_state.expanded_pet_id = None

    # Створюємо сітку (3 колонки)
    cols = st.columns(3)
    
    for idx, pet in enumerate(st.session_state.pets_db):
        with cols[idx % 3]:
            st.image(pet["img"], use_container_width=True)
            st.subheader(pet["name"])
            
            # Кольорові статуси
            if pet["status"] == "Шукає дім":
                st.success(f"🟢 {pet['status']}")
            else:
                st.warning(f"🟡 {pet['status']}")
            
            # Керування кнопкою "Детальніше / Закрити"
            if st.session_state.expanded_pet_id == pet["id"]:
                if st.button("❌ Закрити", key=f"btn_close_{pet['id']}"):
                    st.session_state.expanded_pet_id = None
                    st.rerun()
            else:
                if st.button("📖 Детальніше", key=f"btn_open_{pet['id']}"):
                    # Саме тут магія: ми записуємо ID, і Streamlit перемальовує все,
                    # закриваючи попередню анкету
                    st.session_state.expanded_pet_id = pet["id"]
                    st.rerun()

    # ВІДОБРАЖЕННЯ ДЕТАЛЬНОЇ АНКЕТИ (Тільки для обраної тварини)
    if st.session_state.expanded_pet_id is not None:
        selected_pet = next((p for p in st.session_state.pets_db if p["id"] == st.session_state.expanded_pet_id), None)
        
        if selected_pet:
            st.divider()
            col_img, col_txt = st.columns([1, 1.5])
            
            with col_img:
                st.image(selected_pet["img"], use_container_width=True)
            
            with col_txt:
                st.header(f"Анкета: {selected_pet['name']}")
                st.write(f"**Вік:** {selected_pet['age']} р.")
                st.write(f"**Про тварину:** {selected_pet['desc']}")
                
                st.info("📩 **Подати заявку на адапцію**")
                with st.form(f"adopt_form_{selected_pet['id']}"):
                    u_contact = st.text_input("Ваш контакт (TG/Phone)")
                    u_msg = st.text_area("Кілька слів про себе")
                    if st.form_submit_button("Відправити заявку"):
                        if u_contact:
                            st.toast(f"Заявка на {selected_pet['name']} прийнята!")
                            time.sleep(1)
                            st.session_state.expanded_pet_id = None # Закриваємо після відправки
                            st.rerun()
                        else:
                            st.error("Вкажіть контакт!")