import streamlit as st
import pandas as pd
import numpy as np

st.title("BFN Map Visualization")
st.markdown("### Black Farmers Network Locations in Georgia")

# Define coordinates
coordinates = [
    ("Rountree Farm", (30.8730159, -83.54965659999999)),
    ("Morgan Farm", (31.9981596, -84.2278796)),
    ("Lewis Clark Farm", (30.8417409, -83.8473015)),
    ("Fowler Farm", (31.5282489, -83.8897057)),
    ("Hubert Farm", (33.2882621, -83.03613759999999)),
    ("Kindler Farm", (31.2008218, -84.7315563)),
    ("Charleston-Allen Farm", (33.5794186, -83.46435509999999)),
    ("Garfield Hall Farm", (32.3595678, -81.77870209999999)),
    ("Gilliard Farm", (31.2624169, -81.6035062)),
    ("Williams Farm", (30.8365815, -83.9787808)),
    ("Cooper Farm", (33.088805, -81.9534815)),
    ("Stephens Farm", (31.5439375, -84.2278796))
]

# Calculate the center of the map
center_lat = sum(coord[1][0] for coord in coordinates) / len(coordinates)
center_lon = sum(coord[1][1] for coord in coordinates) / len(coordinates)

# Create a Folium map centered on Georgia
m = folium.Map(location=[center_lat, center_lon], 
               zoom_start=7,
               tiles='CartoDB positron')  # Using a clean, modern map style

# Add markers for each location
for name, coord in coordinates:
    folium.CircleMarker(
        location=coord,
        radius=8,
        popup=f'{name}',
        color='#FF4B4B',  # Red color for visibility
        fill=True,
        fill_color='#FF4B4B',
        fill_opacity=0.7,
        weight=2
    ).add_to(m)

# Add a title to the map
title_html = '''
             <div style="position: fixed; 
                         top: 10px; 
                         left: 50px; 
                         width: 300px; 
                         height: 90px; 
                         z-index:9999; 
                         background-color: rgba(255, 255, 255, 0.8); 
                         border-radius: 10px; 
                         padding: 10px;">
                 <h4>Black Farmers Network Locations</h4>
                 <p>Interactive map showing BFN locations across Georgia</p>
             </div>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Display the map
    st_folium(m, width=800, height=600)

with col2:
    # Add some statistics or information

    northernmost_farm, northernmost_coord = max(coordinates, key=lambda coord: coord[1][0])
    southernmost_farm, southernmost_coord = min(coordinates, key=lambda coord: coord[1][0])
    easternmost_farm, easternmost_coord = max(coordinates, key=lambda coord: coord[1][1])
    westernmost_farm, westernmost_coord = min(coordinates, key=lambda coord: coord[1][1])

    st.markdown("### Location Statistics")
    st.write(f"Total Locations: {len(coordinates)}")
    st.write("Geographic Distribution:")
    st.write(f"- Northernmost: {northernmost_farm} ({northernmost_coord[0]:.2f}°N)")
    st.write(f"- Southernmost: {southernmost_farm} ({southernmost_coord[0]:.2f}°N)")
    st.write(f"- Easternmost: {easternmost_farm} ({easternmost_coord[1]:.2f}°W)")
    st.write(f"- Westernmost: {westernmost_farm} ({westernmost_coord[1]:.2f}°W)")

