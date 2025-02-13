import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os

st.set_page_config(layout="wide")

# Title and Introduction
st.markdown("<h1 style='text-align: center; margin-bottom: 10px'>Black Farmers Network Centennial Farms</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 10px;'>What are Black Owned Centennial Farms?</h3>", unsafe_allow_html=True)
st.markdown(
    "Black Owned Centennial Farms are farms that have been owned and operated by the same family for 100 years or more. "
    "These farms have a rich history tied to the broader history of Black Americans in the U.S. "
    "The Black Farmers Network (BFN) works to preserve and promote these farms, supporting the families that own them. "
    "Currently, there are 12 centennial farms in Georgia. Please interact with the map to learn more!"
)
st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Black Farmers Network Centennial Farms Locations in Georgia</h3>", unsafe_allow_html=True)

# Define farm coordinates
coordinates = [
    ("Rountree Farm", (30.8730159, -83.5496566)),
    ("Morgan Farm", (31.9981596, -84.2278796)),
    ("Lewis Clark Farm", (30.8417409, -83.8473015)),
    ("Fowler Farm", (31.5282489, -83.8897057)),
    ("Hubert Farm", (33.2882621, -83.0361376)),
    ("Kindler Farm", (31.2008218, -84.7315563)),
    ("Charleston-Allen Farm", (33.5794186, -83.4643551)),
    ("Garfield Hall Farm", (32.3595678, -81.7787021)),
    ("Gilliard Farm", (31.2624169, -81.6035062)),
    ("Williams Farm", (30.8365815, -83.9787808)),
    ("Cooper Farm", (33.088805, -81.9534815)),
    ("Stephens Farm", (31.5439375, -84.2278796))
]

# Farm descriptions
farm_descriptions = {
    "Rountree Farm": "Founded in 1891 by John Willis Rountree, a skilled carpenter and farmer. The farm received the Centennial Family Farm Award in 1994.",
    "Morgan Farm": "Established in 1886 by former slave Nathan Morgan, awarded the Centennial Family Farm Award in 1995, and listed in the National Register of Historic Places in 1998.",
    "Lewis Clark Farm": "Founded in 1875 by Lewis Clark, originally producing cotton, corn, sweet potatoes, and sugar cane. Still family-owned today.",
    "Fowler Farm": "Reverend James Fowler acquired 202 acres in 1888 and became a leading cotton producer. His descendants expanded production to peanuts, wheat, and soybeans.",
    "Hubert Farm": "Founded by former slave Zach Hubert, the farm has received multiple Centennial Farm Awards and serves as an educational landmark for African American farming history.",
    "Kindler Farm": "Littleton Kinder purchased 240 acres from A.L. Bowen. The farm played a critical role in African American land protection during the Jim Crow era.",
    "Charleston-Allen Farm": "Founded in 1890 by Anna Charleston, an enslaved woman 30 years prior. It evolved into a 100-acre tree farm in Morgan County.",
    "Garfield Hall Farm": "Acquired in 1928, this family farm has produced cotton, corn, tobacco, and peanuts. Portions of the land are now used for tree farming.",
    "Gilliard Farm": "Jupiter Gilliard, a formerly enslaved man, founded this farm in 1874. It transformed into an organic farm and won the Centennial Family Farm Award in 2012.",
    "Williams Farm": "Established in 1883 by Charles Cockrell, the farm has remained in the family for generations, producing cotton, peanuts, pecans, and cattle.",
    "Cooper Farm": "Frank Cooper Sr. purchased this farm in 1885. Today, it remains a symbol of long-term Black land ownership, producing cotton and peanuts.",
    "Stephens Farm": "Titus Stephens acquired this land after the Civil War. His descendants still own the 99-acre farm, which remains committed to sustainable farming."
}

# Calculate map center
center_lat = sum(lat for _, (lat, lon) in coordinates) / len(coordinates)
center_lon = sum(lon for _, (lat, lon) in coordinates) / len(coordinates)

# Convert images to base64 for display
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Load images
image_dir = "images"
base64_images = []
image_files = sorted(os.listdir(image_dir))
for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    if os.path.isfile(image_path):
        base64_images.append(image_to_base64(image_path))

# Create the Folium map with OpenStreetMap
m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="OpenStreetMap")

# Add farm markers
for index, (name, coord) in enumerate(coordinates):
    popup_html = f'''
        <div style="text-align: center;">
            <h4>{name}</h4>
            <img src="data:image/png;base64,{base64_images[index]}" width="150px">
            <br>
            <p>{farm_descriptions.get(name, "Description not available")}</p>
        </div>
    '''
    folium.Marker(
        location=coord,
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color="green", icon="tree", prefix="fa")
    ).add_to(m)

# Add a title overlay
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

# Farm detail page handling
selected_farm = st.query_params.get("farm", "").replace("_", " ")
if selected_farm in dict(coordinates):
    st.title(selected_farm)
    st.markdown("### About the Farm")
    st.write(farm_descriptions.get(selected_farm, "Description coming soon..."))
    
    if st.button("← Back to Map"):
        st.query_params.clear()
        st.rerun()
else:
    # Display map and farm list
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st_folium(m, width=800, height=600)
    
    with col2:
        st.markdown("### Farm Locations")
        for index, (name, _) in enumerate(coordinates, start=1):
            st.write(f"{index}. {name}")
