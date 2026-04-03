import folium
import streamlit as st

def create_pet_map(center_lat=48.4647, center_lon=35.0461):
    bounds = [[47.70, 33.90], [49.25, 36.20]]
    m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=9,
        min_zoom=9,
        max_bounds=True,
        min_lat=bounds[0][0], max_lat=bounds[1][0],
        min_lon=bounds[0][1], max_lon=bounds[1][1]
    )
    m.fit_bounds(bounds)
    folium.Circle(
        radius=80000,
        location=[center_lat, center_lon],
        color="crimson",
        fill=True,
        fill_opacity=0.1,
        interactive=False,
    ).add_to(m)
    return m