import time
import streamlit as st
import pandas as pd
import os
from src.database import SessionLocal 
from src.model import Animal 

def show():
    st.title("⚙️ Панель волонтера")
    st.write("Керування базою тварин притулку через SQLite")

    # ВІДКРИВАЄМО БД
    db = SessionLocal()

    with st.expander("➕ Додати нову тварину в базу", expanded=False):
        with st.form("add_new_pet_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Кличка тварини*")
                new_age = st.number_input("Приблизний вік", min_value=0, max_value=25, value=1)
                new_gender = st.selectbox("Стать", ["Хлопчик", "Дівчинка"])
            
            with col2:
                new_status = st.selectbox("Статус", ["Шукає дім", "На адаптації", "Прилаштована", "На лікуванні"])
                new_contact = st.text_input("Контакт волонтера*")
                new_photo = st.file_uploader("Завантажте фото*", type=["jpg", "jpeg", "png"])
            
            new_desc = st.text_area("Опис тварини (прикмети, характер)")
            submit_new = st.form_submit_button("🚀 Додати тварину в базу")

            if submit_new:
                if new_name and new_photo and new_contact:
                    os.makedirs("photos", exist_ok=True)
                    file_path = f"photos/{new_photo.name}"
                    with open(file_path, "wb") as f:
                        f.write(new_photo.getbuffer())

                    new_entry = Animal(
                        name=new_name,
                        path=file_path,
                        age=new_age,
                        gender=new_gender,
                        status=new_status,
                        contact=new_contact,
                        description=new_desc
                    )
                    
                    try:
                        db.add(new_entry)
                        db.commit()
                        st.success(f"Тварину {new_name} успішно додано!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        db.rollback()
                        st.error(f"Помилка при додаванні: {e}")
                else:
                    st.error("Будь ласка, заповніть обов'язкові поля (*).")

    st.divider()

    st.subheader("📝 Редагування та зміна статусів")
    
    query = db.query(Animal).all()
    if query:
        data = [
            {
                "id": animal.id,
                "name": animal.name,
                "age": animal.age,
                "gender": animal.gender,
                "status": animal.status,
                "contact": animal.contact,
                "description": animal.description,
                "path": animal.path
            } for animal in query
        ]
        df = pd.DataFrame(data)

        #редактор таблиці
        edited_df = st.data_editor(
            df,
            column_config={
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "name": st.column_config.TextColumn("Ім'я (Кличка)"),
                "path": st.column_config.TextColumn("Шлях до фото"),
                "status": st.column_config.SelectboxColumn(
                    "Статус",
                    options=["Шукає дім", "На адаптації", "Прилаштована", "На лікуванні"],
                    required=True,
                ),
                "gender": st.column_config.SelectboxColumn("Стать", options=["Хлопчик", "Дівчинка"]),
                "age": st.column_config.NumberColumn("Вік"),
                "contact": st.column_config.TextColumn("Контакт"),
                "description": st.column_config.TextColumn("Опис")
            },
            disabled=["id"],
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )

        #логіка збереження змін
        if st.button("💾 Зберегти всі зміни"):
            try:
                for index, row in edited_df.iterrows():
                    db_animal = db.query(Animal).filter(Animal.id == row['id']).first()
                    if db_animal:
                        db_animal.name = row["name"]
                        db_animal.path = row["path"]
                        db_animal.status = row["status"]
                        db_animal.gender = row["gender"]
                        db_animal.age = row["age"] 
                        db_animal.contact = row["contact"]
                        db_animal.description = row["description"]
                
                db.commit()
                st.success("Базу даних успішно оновлено! ✨")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                db.rollback()
                st.error(f"Помилка при збереженні: {e}")

    st.divider()
    st.subheader("📊 Поточні показники")
    
    total = db.query(Animal).count()
    ready = db.query(Animal).filter(Animal.status == "Шукає дім").count()
    done = db.query(Animal).filter(Animal.status == "Прилаштована").count()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Всього в базі", total)
    c2.metric("Готові до всиновлення", ready)
    c3.metric("Знайшли родину", done, delta="🎉")

    db.close()

if __name__ == "__main__":
    show()