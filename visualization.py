import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import base64
import os

st.set_page_config(layout="wide")

# st.title("BFN Map Visualization")
# st.markdown("### Black Farmers Network Locations in Georgia")

st.markdown("<h1 style='text-align: center; margin-bottom: 10px'>Black Farmers Network Centennial Farms</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 10px; '>What are Black Owned Centennial Farms?</h3>", unsafe_allow_html=True)
st.markdown("Black Owned Centennial Farms are farms that have been owned and operated by the same family for 100 years or more. These farms have been passed down through generations and have a rich history that is often tied to the broader history of Black Americans in the United States. The Black Farmers Network (BFN) is an organization that works to preserve and promote these historic farms, and to support the families that own them. Currently, there are 12 centennial farms in Georgia which demonstrates the rarity of these farms. Please interact with the map to learn more about Black Owned Centennial Farms! ")
st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Black Farmers Network Centennial Farms Locations in Georgia</h3>", unsafe_allow_html=True)

dataset = pd.read_csv("preprocessed_bfn.csv")


# Define coordinates

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
center_lat = sum(lat for _, (lat, lon) in coordinates) / len(coordinates)
center_lon = sum(lon for _, (lat, lon) in coordinates) / len(coordinates)

# Create a dictionary for farm descriptions (you can replace these placeholder descriptions later)
farm_descriptions = {
    "Rountree Farm": "Description for Rountree Farm...",
    "Morgan Farm": "Description for Morgan Farm...",
    "Lewis Clark Farm": "Description for Lewis Clark Farm...",
    # ... Add descriptions for all farms ...
}


# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Directory containing images
image_dir = "images"
base64_images = []

# Get list of image files and sort to maintain order
image_files = sorted(os.listdir(image_dir))

# Convert each image to base64
for i, image_file in enumerate(image_files):
    image_path = os.path.join(image_dir, image_file)
    if os.path.isfile(image_path):
        base64_images.append(image_to_base64(image_path))


# Create a Folium map centered on Georgia
m = folium.Map(location=[center_lat, center_lon], 
               zoom_start=7,
               tiles='CartoDB Positron')

folium.TileLayer(
    tiles='https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.{ext}', 
    attr='&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors', 
    min_zoom=0, 
    max_zoom=18, 
    ext='png', 
    name="Stadia_StamenTerrain"
).add_to(m)

# Add markers for each location
for index, (name, coord) in enumerate(coordinates):
    # Create HTML for the popup with a link
    popup_html = popup_html = f'''
        <div style="text-align: center;">
            <h4>{name}</h4>
            <img src="data:image/png;base64,{base64_images[index]}" width="150px">
            <br>
            <a href="?farm={name.replace(' ', '_')}" target="_self">View Details</a>
        </div>
    '''
    
    folium.Marker(
    location=coord,
    popup=folium.Popup(popup_html, max_width=200),
    icon=folium.Icon(color="red", icon="star", prefix="fa")  # Green star icon
    ).add_to(m)


# Add a title to the map
title_html = '''
             <div style="position: fixed; 
                         top: 10px; 
                         left: 50px; 
                         width: 300px; 
                         height: 90px; 
                         z-index:9999; 
                         background-color: rgba(243, 229, 171, 0.8); 
                         border-radius: 10px; 
                         padding: 10px;">
                 <h4>Black Farmers Network Locations</h4>
                 <p>Interactive map showing BFN locations across Georgia</p>
             </div>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Add farm detail page handling
selected_farm = st.query_params.get("farm", "").replace("_", " ")
if selected_farm in dict(coordinates):
    st.title(selected_farm)
    
    # Display farm description (you can replace this with real descriptions later)
    st.markdown("### About the Farm")
    st.write(farm_descriptions.get(selected_farm, "Description coming soon..."))
    
    # Add a back button
    if st.button("← Back to Map"):
        st.query_params.clear()
        st.rerun()
else:
    # Original map view code
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st_folium(m, width=800, height=600)
    
    with col2:
        # Replace "Location Statistics" with a numbered list of farm names
        st.markdown("### Farm Locations")
        for index, (name, _) in enumerate(coordinates, start=1):
            st.write(f"{index}. {name}")