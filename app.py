import streamlit as st

st.set_page_config(page_title="Rescue Bobik", page_icon="logo_dniproanimals.png", layout="centered")

st.markdown("""
<style>
    [data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        height: 64vh;
    }

    [data-testid="stSidebarUserContent"] > div:last-child {
        margin-top: 100%;
        padding-bottom: 40px;
    }

    .stButton>button {
        border-radius: 15px;
        height: 60px;
        transition: 0.3s;
    }
    [data-testid="stSidebar"] .stButton>button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none;
        font-weight: bold;
        margin-bottom: 250px;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #e03e3e !important;
        transform: scale(1.02);
    }
    [data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

#ініціалізація бази
if 'pets_db' not in st.session_state:
    st.session_state.pets_db = [
        {"id": 0, "name": "Барон", "breed": "Кіт", "age": 2, "status": "Шукає дім", "desc": "Знайдений на Перемозі.", "img": "photo/0E1A8113.jpeg"},
        {"id": 1, "name": "Альма", "breed": "Собака", "age": 1, "status": "На адаптації", "desc": "Лагідна, вакцинована.", "img": "photo/0E1A8132.jpeg"},
        {"id": 2, "name": "Рекс", "breed": "Собака", "age": 5, "status": "Шукає дім", "desc": "Охоронець.", "img": "photo/0E1A8136.jpeg"},
        {"id": 3, "name": "Мурчик", "breed": "Кіт", "age": 3, "status": "Шукає дім", "desc": "Дуже грайливий.", "img": "photo/0E1A8159.jpeg"},
    ]

#навігація
pg = st.navigation({
    "Користувачам": [
        st.Page("views/home.py", title="Головна", icon="🏠", default=True),
        st.Page("views/found.py", title="Я знайшов тварину", icon="🐕"),
        st.Page("views/lost.py", title="Я шукаю тварину", icon="😢"),
        st.Page("views/catalog.py", title="Притулок", icon="🐈"),
    ],
    "Волонтерам": [
        st.Page("views/admin.py", title="Адмін-панель", icon="⚙️"),
    ]
})
pg.run()

#ФУТЕР 
st.sidebar.divider()
st.sidebar.subheader("Підтримка проєкту")

if st.sidebar.button("💰 Зробити донат", key="side_donate"):
    st.sidebar.info("Тут бекендер підключить Monobank")

try:
    st.sidebar.image("logo_dniproanimals.png", width=230)
except FileNotFoundError:
    st.sidebar.error("Файл logo_dniproanimals.png не знайдено!")