import streamlit as st
import requests
import pandas as pd
import time

# 1. Налаштування сторінки
st.set_page_config(
    page_title="Пошук Бобіка", 
    page_icon="🐾", 
    layout="centered"
)

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

# Ініціалізація стану сторінок
if 'page' not in st.session_state: 
    st.session_state.page = 'main'

if 'submission_success' not in st.session_state: 
    st.session_state.submission_success = False

# СТОРІНКА 1: ГОЛОВНА
if st.session_state.page == 'main': 
    st.session_state.submission_success = False 

    st.title("🐾 Служба порятунку Бобиків") 
    st.write("Виберіть дію, щоб продовжити:") 

    st.write("") 
    col1, col2 = st.columns(2) 

    with col1: 
        if st.button("🐕 Я знайшов собаку"): 
            st.session_state.page = 'found' 
            st.rerun() 

    with col2: 
        if st.button("😢 Я шукаю собаку"): 
            st.session_state.page = 'lost' 
            st.rerun()

# СТОРІНКА 2: ЗНАЙШОВ СОБАКУ
elif st.session_state.page == 'found': 
    if st.button("⬅️ Назад на головну"): 
        st.session_state.page = 'main' 
        st.rerun() 

    st.subheader("Реєстрація знайденого собаки") 
    st.write("Будь ласка, заповніть форму. Це допоможе господареві знайти вихованця.") 

    if st.session_state.submission_success: 
        st.markdown('<p class="big-success">🎉 Дякуємо за допомогу! Ви робите добру справу. 🎉</p>', unsafe_allow_html=True) 
        st.write("Дані успішно завантажені в базу. Волонтери скоро перевірять анкету.") 

        if st.session_state.get('show_balloons', False): 
            st.balloons() 
            st.session_state.show_balloons = False 

    else: 
        with st.form("found_form"): 
            name = st.text_input("Ім'я (якщо відгукується, або 'Невідомо')") 
            age = st.number_input("Приблизний вік (років)", min_value=0, max_value=20, step=1) 
            description = st.text_area("Опис (забарвлення, нашийник, прикмети)") 
            contact = st.text_input("Ваш контакт (Telegram/Телефон)") 

            col_lat, col_lon = st.columns(2) 
            with col_lat: 
                lat = st.text_input("Широта (lat)", value="48.4647") 
            with col_lon: 
                lon = st.text_input("Довгота (lon)", value="35.0461") 

            photo = st.file_uploader("Фотографія собаки", type=["jpg", "png", "jpeg"]) 
            submit_found = st.form_submit_button("Відправити до бази") 

        if submit_found: 
            if photo and contact: 
                files = {"file": (photo.name, photo.getvalue(), photo.type)} 
                data = {
                    "name": name, "age": age, "description": description,
                    "lat": float(lat), "lon": float(lon), "contact": contact
                } 
                try: 
                    response = requests.post("http://localhost:8000/upload/found", files=files, data=data) 
                    if response.status_code == 200: 
                        st.session_state.submission_success = True 
                        st.session_state.show_balloons = True 
                        st.rerun() 
                    else: 
                        st.error(f"Помилка бекенду: {response.text}") 
                except requests.exceptions.ConnectionError: 
                    st.error("Бекенд не відповідає. Запустіть сервер Uvicorn!") 
            else:
                st.error("Будь ласка, додайте фото та контакт!")

# СТОРІНКА 3: ШУКАЮ СОБАКУ
elif st.session_state.page == 'lost': 
    if st.button("⬅️ Назад на головну"): 
        st.session_state.page = 'main' 
        st.rerun() 

    st.subheader("Пошук зниклого вихованця") 
    st.write("Заповніть анкету, і ми покажемо схожих собак поруч.") 

    with st.form("lost_form"): 
        name = st.text_input("Ім'я собаки") 
        age = st.number_input("Вік", min_value=0, max_value=20, step=1) 
        description = st.text_area("Прикмети") 
        contact = st.text_input("Ваш контакт") 
        
        col_lat, col_lon = st.columns(2) 
        with col_lat: 
            lat = st.text_input("Широта (де загубився)", value="48.4647") 
        with col_lon: 
            lon = st.text_input("Довгота (де загубився)", value="35.0461")

        photo = st.file_uploader("Фото вихованця", type=["jpg", "png", "jpeg"]) 
        submit_lost = st.form_submit_button("Розпочати пошук") 

    if submit_lost: 
        if photo and contact: 
            files = {"file": (photo.name, photo.getvalue(), photo.type)} 
            data = {
                "name": name, "age": age, "description": description,
                "lat": float(lat), "lon": float(lon), "contact": contact
            } 
            try: 
                response = requests.post("http://localhost:8000/upload/lost", files=files, data=data) 
                if response.status_code == 200: 
                    st.success("Ось де бачили схожих собак:") 
                    mock_data = pd.DataFrame({
                        'lat': [48.4647, 48.4700, 48.4550],
                        'lon': [35.0461, 35.0500, 35.0300]
                    })
                    st.map(mock_data, zoom=12) 
                else: 
                    st.error(f"Помилка бекенду: {response.text}") 
            except requests.exceptions.ConnectionError: 
                st.error("Сервер бекенду не запущений!") 
        else:
            st.error("Заповніть контакт та додайте фото!")