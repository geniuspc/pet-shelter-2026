import streamlit as st
import requests
import pandas as pd  # Понадобится для фейковой карты
import time  # Для небольшой задержки перед анимацией (чтобы юзер успел прочитать текст)

# Настройка страницы
st.set_page_config(page_title="Поиск Бобика", page_icon="🐶", layout="centered")

# Кастомный CSS для больших и красивых кнопок
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button {width: 100%; border-radius: 10px; height: 60px; font-size: 18px; font-weight: bold;}
    /* Стилизация текста успеха, чтобы он был по центру рядом с анимацией */
    .big-success {
        font-size: 24px;
        color: #28a745;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Инициализация "роутера" (переключателя страниц)
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Инициализация флага успеха для анимации
if 'submission_success' not in st.session_state:
    st.session_state.submission_success = False

# ==========================================
# СТРАНИЦА 1: ГЛАВНАЯ
# ==========================================
if st.session_state.page == 'main':
    # Сбрасываем флаг успеха при возврате на главную
    st.session_state.submission_success = False
    
    st.title("🐾 Служба спасения Бобиков")
    st.write("Выберите действие, чтобы продолжить:")
    
    st.write("") # Отступ
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🐕 Я нашел собаку"):
            st.session_state.page = 'found'
            st.rerun() # Перезапускает скрипт, чтобы показать новую страницу
            
    with col2:
        if st.button("😢 Я ищу собаку"):
            st.session_state.page = 'lost'
            st.rerun()

# ==========================================
# СТРАНИЦА 2: НАШЕЛ СОБАКУ
# ==========================================
elif st.session_state.page == 'found':
    if st.button("⬅️ Назад на главную"):
        st.session_state.page = 'main'
        st.rerun()
        
    st.subheader("Регистрация найденной собаки")
    st.write("Пожалуйста, заполните форму. Это поможет хозяину найти питомца.")
    
    # Если данные успешно отправлены, показываем текст
    if st.session_state.submission_success:
        st.markdown('<p class="big-success">🎉 Спасибо за помощь! Вы делаете доброе дело. 🎉</p>', unsafe_allow_html=True)
        st.write("Данные успешно загружены в базу. Волонтеры скоро проверят анкету.")
        
        # --- ИСПРАВЛЕНИЕ ЗДЕСЬ: Запускаем шарики после перезагрузки ---
        if st.session_state.get('show_balloons', False):
            st.balloons()
            # Сразу отключаем флаг, чтобы шарики не летели снова, если пользователь куда-то кликнет
            st.session_state.show_balloons = False 
            
    else:
        with st.form("found_form"):
            name = st.text_input("Имя (если откликается, или 'Неизвестно')")
            age = st.number_input("Примерный возраст (лет)", min_value=0, max_value=20, step=1)
            description = st.text_area("Описание (окрас, ошейник, приметы)")
            contact = st.text_input("Ваш контакт (Telegram/Телефон)")
            
            col_lat, col_lon = st.columns(2)
            with col_lat:
                lat = st.text_input("Широта (lat)", value="48.4647")
            with col_lon:
                lon = st.text_input("Долгота (lon)", value="35.0461")
                
            status = st.selectbox("Статус", ["Найдена", "На передержке"])
            photo = st.file_uploader("Фотография собаки", type=["jpg", "png", "jpeg"])
            
            submit_found = st.form_submit_button("Отправить в базу")
            
       # Логика обработки нажатия кнопки
        if submit_found:
            if photo and contact:
                # 1. Подготавливаем данные для отправки на бэкенд
                files = {"file": (photo.name, photo.getvalue(), photo.type)}
                data = {
                    "name": name,
                    "age": age,
                    "description": description,
                    "contact": contact,
                    "lat": lat,
                    "lon": lon
                }
                
                try:
                    # 2. Стучимся на сервер твоего бэкендера (на порт 8000)
                    response = requests.post("http://localhost:8000/upload/found", files=files, data=data)
                    
                    # 3. Проверяем ответ
                    if response.status_code == 200:
                        # Сервер всё сохранил! Показываем шарики и успех
                        st.session_state.submission_success = True
                        st.session_state.show_balloons = True 
                        st.rerun()
                    else:
                        # Бэкенд вернул ошибку (например, не тот формат данных)
                        st.error(f"Бэкенд ругается: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                     # Если бэкендер еще не запустил сервер или он упал
                     st.error("Бэкенд не отвечает. Пните бэкендера, пусть проверит сервер!")
                     
            else:
                st.error("Пожалуйста, прикрепите фото и оставьте контакт.")
# ==========================================
# СТРАНИЦА 3: ИЩУ СОБАКУ
# ==========================================
elif st.session_state.page == 'lost':
    if st.button("⬅️ Назад на главную"):
        st.session_state.page = 'main'
        st.rerun()
        
    st.subheader("Поиск пропавшего питомца")
    st.write("Заполните приметы вашей собаки, и мы покажем, где видели похожих.")
    
    with st.form("lost_form"):
        name = st.text_input("Имя питомца")
        age = st.number_input("Возраст (лет)", min_value=0, max_value=20, step=1)
        description = st.text_area("Описание (порода, особые приметы)")
        contact = st.text_input("Ваш контакт для связи")
        photo = st.file_uploader("Фотография вашей собаки", type=["jpg", "png", "jpeg"])
        
        submit_lost = st.form_submit_button("Начать поиск")
        
    # Логика ПОСЛЕ нажатия кнопки "Начать поиск"
    if submit_lost:
        if photo and contact:
            # Тут анимация "снега" st.snow() смотрелась бы странно,
            # поэтому здесь просто показываем результат.
            st.success("Мы проанализировали базу! Вот где видели собак, похожих на вашу:")
            
            # ФЕЙКОВЫЕ ДАННЫЕ ДЛЯ КАРТЫ (Mock-up для жюри)
            mock_data = pd.DataFrame({
                'lat': [48.4647, 48.4700, 48.4550],
                'lon': [35.0461, 35.0500, 35.0300],
                'similarity': ['98%', '85%', '70%']
            })
            
            # Встроенная карта Streamlit
            st.map(mock_data, zoom=12)
            
            st.info("Позже здесь будут выводиться реальные фотографии найденных собак от нашего бэкенда.")
        else:
            st.error("Для поиска нейросетью нам обязательно нужно фото собаки и ваши контакты.")

            