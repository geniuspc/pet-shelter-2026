import streamlit as st
import time

#ФУНКЦІЯ МОДАЛЬНОГО ВІКНА
@st.dialog("Детальна інформація")
def show_pet_details(pet):
    # Робимо дві колонки всередині поп-апу
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.image(pet["img"], use_container_width=True)
    
    with col2:
        st.header(pet["name"])
        st.write(f"**Вік:** {pet['age']} р.")
        st.write(f"**Опис:** {pet['desc']}")
        st.write(f"**Статус:** {pet['status']}")
    
    st.divider()
    st.subheader("📩 Подати заявку на адапцію")
    
    with st.form(f"adopt_form_{pet['id']}"):
        u_contact = st.text_input("Ваш контакт (TG/Телефон)")
        u_msg = st.text_area("Кілька слів про себе")
        submit = st.form_submit_button("🏠 Хочу усиновити")
        
        if submit:
            if u_contact:
                st.success(f"Заявка на {pet['name']} прийнята! Волонтери скоро зв'яжуться з вами.")
                time.sleep(2)
                st.rerun() # Закриває вікно після успіху
            else:
                st.error("Вкажіть, будь ласка, контакт!")

#ОСНОВНИЙ КОД СТОРІНКИ
def show():
    if st.button("⬅️ Назад"):
        st.switch_page("views/home.py")

    st.title("🏠 Наші підопічні")
    st.write("Тварини, які чекають на нову родину")

    # Створюємо сітку карток
    cols = st.columns(3)
    for idx, pet in enumerate(st.session_state.pets_db):
        with cols[idx % 3]:
            st.image(pet["img"], use_container_width=True)
            st.subheader(pet["name"])
            
            if pet["status"] == "Шукає дім":
                st.success(f"🟢 {pet['status']}")
            else:
                st.warning(f"🟡 {pet['status']}")
            
            # При натисканні викликаємо діалогове вікно
            if st.button("📖 Детальніше", key=f"open_{pet['id']}"):
                show_pet_details(pet)

if __name__ == "__main__":
    show()