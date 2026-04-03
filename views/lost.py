import streamlit as st
import time
import folium
from streamlit_folium import st_folium
from utils import create_pet_map

st.set_page_config(page_title="Пошук", page_icon="😢")

if st.button("⬅️ Назад"):
   st.switch_page("views/home.py")

st.subheader("🔍 Пошук вашого улюбленця")
with st.form("lost_form"):
    dog_name = st.text_input("Кличка")
    lost_contact = st.text_input("Ваш контакт")
    lost_photo = st.file_uploader("Фото для ШІ", type=["jpg", "png"])
    submit = st.form_submit_button("🚀 Шукати")

if submit and lost_photo:
    st.info("Аналізуємо...")
    time.sleep(1)
    results_map = create_pet_map()
    points = [{"loc": [48.475, 35.06], "txt": "95%"}, {"loc": [48.44, 35.02], "txt": "80%"}]
    for p in points:
        folium.Marker(p["loc"], popup=p["txt"], icon=folium.Icon(color='green')).add_to(results_map)
    st_folium(results_map, width=700, height=400)