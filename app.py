import streamlit as st
from src.payment import create_payment
import uuid

from src.database import engine, Base
from src.model import Animal, Location, Match
Base.metadata.create_all(bind=engine)

st.set_page_config(page_title="Animal Rescue", page_icon="logo_dniproanimals.png", layout="centered")

st.markdown("""
<style>
    [data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        height: 60vh;
    }

    [data-testid="stSidebarUserContent"] > div:last-child {
        margin-top: 0px;
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
        margin-bottom: 10px;
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

with st.sidebar:
    st.header("Підтримати притулок 🍯")
    st.write("Ваші донати допомагають купувати корм та ліки.")
    
    amount = st.number_input("Сума донату (грн)", min_value=10, value=100)
    
    if st.button("💳 Сформувати рахунок"):
        # Генеруємо рандомний ID для платежу
        order_id = f"donate_{uuid.uuid4().hex[:8]}"
        
        with st.spinner("Зв'язуємося з банком..."):
            res = create_payment(order_id, amount)
            
        if "error" in res:
            st.error(res["error"])
            st.info("Перевірте, чи вставлений правильний токен у src/payment.py")
        else:
            # Отримуємо посилання на оплату
            payment_url = res.get("pageUrl")
            if payment_url:
                st.success("Рахунок створено!")
                # Streamlit не може сам відкрити вкладку, тому створюємо кнопку-посилання
                st.link_button("👉 Перейти до оплати", payment_url)

try:
    st.sidebar.image("logo_dniproanimals.png", width=230)
except FileNotFoundError:
    st.sidebar.error("Файл logo_dniproanimals.png не знайдено!")