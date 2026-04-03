import streamlit as st
import pandas as pd
import os

def show():
    st.title("⚙️ Панель волонтера")
    st.write("Керування базою тварин притулку")

    #ДОДАВАННЯ НОВОЇ ТВАРИНИ 
    with st.expander("➕ Додати нову тварину в базу", expanded=False):
        with st.form("add_new_pet_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Кличка тварини*")
                new_breed = st.selectbox("Вид", ["Собака", "Кіт", "Інше"])
                new_age = st.number_input("Приблизний вік", min_value=0, max_value=25, value=1)
            
            with col2:
                new_status = st.selectbox("Статус", ["Шукає дім", "На адаптації", "Прилаштована", "На лікуванні"])
                new_photo = st.file_uploader("Завантажте фото*", type=["jpg", "jpeg", "png"])
            
            new_desc = st.text_area("Опис тварини (прикмети, характер)")
            
            submit_new = st.form_submit_button("🚀 Додати тварину в базу")

            if submit_new:
                if new_name and new_photo:
                    new_id = max([p['id'] for p in st.session_state.pets_db]) + 1 if st.session_state.pets_db else 0
 
                    file_path = f"photo/{new_photo.name}"
                    
                    new_entry = {
                        "id": new_id,
                        "name": new_name,
                        "breed": new_breed,
                        "age": new_age,
                        "status": new_status,
                        "desc": new_desc,
                        "img": file_path 
                    }
                    
                    st.session_state.pets_db.append(new_entry)
                    st.success(f"Тварину {new_name} успішно додано! Тепер вона є в каталозі.")
                    st.balloons()
                else:
                    st.error("Будь ласка, вкажіть кличку та завантажте фото.")

    st.divider()

    #РЕДАГУВАННЯ ІСНУЮЧИХ 
    st.subheader("📝 Редагування та зміна статусів")
    
    df = pd.DataFrame(st.session_state.pets_db)

    edited_df = st.data_editor(
        df,
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "img": st.column_config.TextColumn("Шлях до фото"),
            "status": st.column_config.SelectboxColumn(
                "Статус",
                options=["Шукає дім", "На адаптації", "Прилаштована", "На лікуванні"],
                required=True,
            ),
            "breed": st.column_config.SelectboxColumn("Вид", options=["Собака", "Кіт", "Інше"]),
            "age": st.column_config.NumberColumn("Вік"),
            "name": "Кличка",
            "desc": "Опис"
        },
        disabled=["id"],
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic" # Дозволяє видаляти рядки
    )

    if st.button("💾 Зберегти всі зміни"):
        st.session_state.pets_db = edited_df.to_dict('records')
        st.success("Всі зміни збережено!")

    #СТАТИСТИКА
    st.divider()
    st.subheader("📊 Поточні показники")
    c1, c2, c3 = st.columns(3)
    
    total = len(st.session_state.pets_db)
    ready = sum(1 for p in st.session_state.pets_db if p['status'] == "Шукає дім")
    done = sum(1 for p in st.session_state.pets_db if p['status'] == "Прилаштована")
    
    c1.metric("Всього підопічних", total)
    c2.metric("Готові до всиновлення", ready)
    c3.metric("Знайшли родину", done, delta="🎉")

if __name__ == "__main__":
    show()