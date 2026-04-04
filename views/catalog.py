import streamlit as st
import time
from src.database import SessionLocal
from src.model import Animal 

# ФУНКЦІЯ МОДАЛЬНОГО ВІКНА
@st.dialog("Детальна інформація")
def show_pet_details(pet):
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        if pet.path:
            st.image(pet.path, use_container_width=True)
        else:
            st.warning("Фото відсутнє")
    
    with col2:
        st.header(pet.name if pet.name else f"Тваринка #{pet.id}")
        st.write(f"**Вік:** {pet.age} р.")
        st.write(f"**Стать:** {pet.gender}") 
        st.write(f"**Опис:** {pet.description}") 
        st.write(f"**Статус:** {pet.status}")
        st.write(f"**Контакт волонтера:** {pet.contact}")
    
    st.divider()
    st.subheader("📩 Подати заявку на адапцію")
    
    with st.form(f"adopt_form_{pet.id}"):
        u_contact = st.text_input("Ваш контакт (TG/Телефон)")
        u_msg = st.text_area("Кілька слів про себе")
        submit = st.form_submit_button("🏠 Хочу усиновити")
        
        if submit:
            if u_contact:
                st.success(f"Заявка прийнята! Волонтери скоро зв'яжуться з вами.")
                time.sleep(2)
                st.rerun() 
            else:
                st.error("Вкажіть, будь ласка, контакт!")

# ОСНОВА
def show():
    if st.button("⬅️ Назад"):
        st.switch_page("views/home.py")

    st.title("🏠 Наші підопічні")

    db = SessionLocal()
    
    try:
        pets_db = db.query(Animal).all() 
        
        if not pets_db:
            st.info("У базі поки немає тваринок.")
            return

        cols = st.columns(3)
        for idx, pet in enumerate(pets_db):
            with cols[idx % 3]:
                if pet.path:
                    st.image(pet.path, use_container_width=True)
                
                st.subheader(pet.name if pet.name else f"Тваринка #{pet.id}")
                
                if pet.status == "Шукає дім":
                    st.success(f"🟢 {pet.status}")
                elif pet.status == "На адаптації":
                    st.warning(f"🟡 {pet.status}")
                else:
                    st.info(f"⚪ {pet.status}")
                
                if st.button("📖 Детальніше", key=f"open_{pet.id}"):
                    show_pet_details(pet)
                    
    except Exception as e:
        st.error(f"Помилка завантаження бази даних: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    show()