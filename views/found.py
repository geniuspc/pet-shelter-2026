import streamlit as st
import requests
from streamlit_folium import st_folium
from utils import create_pet_map

st.set_page_config(page_title="Знайшов собаку", page_icon="🐕")

if st.button("⬅️ Назад"):
    st.switch_page("views/home.py")

st.subheader("📍 Де ви бачили собаку?")
found_map = create_pet_map()
map_data = st_folium(found_map, width=700, height=400, key="found_map")

clicked_lat, clicked_lon = 48.4647, 35.0461
if map_data and map_data.get("last_clicked"):
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    st.success(f"Обрано координати: {clicked_lat:.4f}, {clicked_lon:.4f}")

with st.form("found_form"):
    name = st.text_input("Ім'я (якщо відомо)")
    age = st.number_input("Приблизний вік", 0, 20, 1)
    desc = st.text_area("Прикмети")
    contact = st.text_input("Ваш контакт")
    lat_input = st.text_input("Широта", value=str(clicked_lat))
    lon_input = st.text_input("Довгота", value=str(clicked_lon))
    photo = st.file_uploader("Фото", type=["jpg", "png", "jpeg"])
    submit = st.form_submit_button("📢 Відправити")

    if submit:
        if photo and contact:
            files = {"file": (photo.name, photo.getvalue(), photo.type)}
            data = {"name": name, "age": age, "description": desc, "lat": float(lat_input), "lon": float(lon_input), "contact": contact}
            try:
                res = requests.post("http://localhost:8000/upload/found", files=files, data=data)
                if res.status_code == 200: st.balloons(); st.success("Готово!")
                else: st.error("Помилка бекенду")
            except: st.error("Сервер не відповідає")