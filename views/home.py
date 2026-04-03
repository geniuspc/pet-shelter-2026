import streamlit as st

def show():
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="font-size: 55px;">🐾 Bobik Rescue</h1>
            <p style="font-size: 20px; color: #888;">Допомагаємо чотирилапим знайти шлях додому в Дніпрі</p>
        </div>
    """, unsafe_allow_html=True)

    #СТАТИСТИКА
    total_pets = len(st.session_state.pets_db)
    looking_for_home = sum(1 for p in st.session_state.pets_db if p['status'] == 'Шукає дім')
    on_adaptation = sum(1 for p in st.session_state.pets_db if p['status'] == 'На адаптації')

    st.write("")
    s1, s2, s3 = st.columns(3)
    s1.metric("Тварин у базі", total_pets)
    s2.metric("Шукають дім", looking_for_home)
    s3.metric("На адаптації", on_adaptation)
    st.write("")
    
    st.divider()

    #основа
    st.subheader("Чим ми можемо допомогти?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🐕 Я знайшов тварину")
            st.write("Побачили самотнього собаку чи кота? Додайте фото та локацію в нашу базу.")
            if st.button("Створити оголошення", key="go_found"):
                st.switch_page("views/found.py")

    with col2:
        with st.container(border=True):
            st.markdown("### 😢 Я шукаю свого друга")
            st.write("Ваш улюбленець зник? Наш ШІ порівняє ваше фото з усіма знахідками у Дніпрі.")
            if st.button("Розпочати пошук", key="go_lost"):
                st.switch_page("views/lost.py")

    st.write("")

    #притулок
    with st.container(border=True):
        c1, c2 = st.columns([1, 2])
        with c1:
            first_pet_img = st.session_state.pets_db[0]["img"]
            st.image(first_pet_img, use_container_width=True) 
        with c2:
            st.markdown("### 🏠 Подаруйте сім'ю")
            st.write("У нашому каталозі десятки чудових тварин, які мріють про люблячих господарів. Подивіться анкети наших підопічних.")
            if st.button("Перейти в каталог притулку", key="go_catalog"):
                st.switch_page("views/catalog.py")

if __name__ == "__main__":
    show()