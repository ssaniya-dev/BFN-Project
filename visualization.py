import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import base64
import os

st.set_page_config(layout="wide")
    
# Initialize session state for tracking clicked farm
if 'selected_farm' not in st.session_state:
    st.session_state.selected_farm = None
if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

# Icon
st.columns(3)[1].image("bfn-top.png")
## Title and Introduction
st.markdown("<h1 style='text-align: center; margin-bottom: 10px'>Black Farmers Network Centennial Farms</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 10px;'>What are Black Owned Centennial Farms?</h3>", unsafe_allow_html=True)
st.markdown("""
Family farms have long been the backbone of Georgia's agricultural landscape, representing more than just agricultural enterprises - they are living repositories of cultural heritage, traditional farming practices, and generational knowledge. These farms, passed down through families over decades and centuries, tell the story of resilience, persistence, and deep connection to the land. This legacy takes on particular significance within the Black farming community, where historical challenges and systemic barriers have made the preservation of family-owned farms both more difficult and more crucial.

The 2022 Census of Agriculture underscores the urgent importance of preserving these agricultural legacies. Out of Georgia's 39,264 farms, only 1,905 (4.8%) are operated by Black/African American producers - a dramatic decline from historical numbers. While 93 percent of these remaining farms are family-owned, they face significant economic challenges, with 42 percent generating less than USD 2,500 in annual sales compared to the state average of $337,189 per farm. These statistics highlight why the recognition and preservation of longstanding Black-owned farms is so vital to maintaining cultural heritage.

The Centennial Family Farm Awards program serves as a crucial initiative in preserving this agricultural heritage by recognizing farms that have remained in the same family for 100 years or more. These centennial farms are more than historical landmarks; they represent living connections to traditional farming practices, cultural knowledge, and community resilience. Each recognized farm tells a unique story of family perseverance, agricultural innovation, and cultural preservation across generations. The program helps ensure these important agricultural legacies are documented, celebrated, and preserved for future generations.

To help visualize and celebrate these important cultural landmarks, we've developed an interactive web platform using Streamlit that maps Georgia's centennial farms. This visualization tool allows users to explore the geographic distribution of these historic farms, learn about their unique histories, and understand their significance in preserving Georgia's agricultural heritage. Through this platform, we aim to highlight the enduring importance of family farms while providing a resource for those interested in learning more about Georgia's rich farming legacy. The map serves not only as a documentation tool but also as a testament to the resilience of family farming traditions and their crucial role in maintaining cultural heritage.

This digital preservation effort becomes even more significant when considering the census data showing 985 new and beginning Black farmers in Georgia. These emerging agriculturists represent hope for the future while building upon the foundation laid by centennial farms. By connecting historical legacy with modern farming practices through our interactive platform, we help ensure that the rich heritage of Black farming in Georgia continues to be preserved, celebrated, and passed down to future generations.
"""
)

st.markdown(f"""
<div style="display: flex; justify-content: center;">
    <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vT9dwiv5jvfKKsn28mh7exTYR_1lVw7-cozgsqvVfhvybURatyPrzu9tyF-MXWgwZ94weCRwdFlz3af/embed?start=false&loop=true&delayms=5000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>Black Farmers Network Centennial Farms Locations in Georgia</h3>", unsafe_allow_html=True)
### Load data
# Load farm data from CSV
try:
    df_farms = pd.read_csv('preprocessed_bfn.csv')
except FileNotFoundError:
    # Fallback to existing descriptions if CSV not found
    df_farms = None

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
    ("Kentavia Williams Farm", (30.8365815, -83.9787808)),
    ("Cooper Farm", (33.088805, -81.9534815)),
    ("Stephens Farm", (31.5439375, -84.2278796)),
    ("Thompson Farm", (33.3205339, -82.08429009999999)),
    ("Gough Family Land LLC.", (33.093870, -82.223732)),
    ("Toomer Farm", (32.4219655, -83.63484299999999))
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
    "Kentavia Williams Farm": "Established in 1883 by Charles Cockrell, the farm has remained in the family for generations, producing cotton, peanuts, pecans, and cattle.",
    "Cooper Farm": "Frank Cooper Sr. purchased this farm in 1885. Today, it remains a symbol of long-term Black land ownership, producing cotton and peanuts.",
    "Stephens Farm": "Titus Stephens acquired this land after the Civil War. His descendants still own the 99-acre farm, which remains committed to sustainable farming.",
    "Thompson Farm": "Thompson Farms, established in 1918, is the oldest African American-owned business in Augusta, Georgia, and received the Georgia Centennial Family Farm award in 2019.",
    "Gough Family Land LLC.": "The Gough Family Farm, established in 1838, has thrived for over 180 years on values of resilience. It received the Centennial Family Farm Award in 2022.",
    "Toomer Farm": "Toomer Farm, with roots dating back to 1900, continues a legacy of resilience, producing diverse crops from century-old trees."
}

# Calculate map center
center_lat = sum(lat for _, (lat, lon) in coordinates) / len(coordinates)
center_lon = sum(lon for _, (lat, lon) in coordinates) / len(coordinates)

## Load images
# Convert images to base64 for display
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
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
        icon=folium.Icon(color="green", icon="wheat-awn", prefix="fa"),
        name=f"{index}:{name}"
    ).add_to(m)

col1, col2 = st.columns([2, 1])
    
with col1:
    map_data = st_folium(m, width=800, height=600)
    # Check if a popup was clicked
    if map_data and 'last_object_clicked' in map_data and map_data['last_object_clicked']:
        popup_content = map_data['last_object_clicked']
        clicked_lat = map_data['last_object_clicked']['lat']
        clicked_lng = map_data['last_object_clicked']['lng']
        
        # Find the closest farm to the clicked coordinates
        min_distance = float('inf')
        selected_farm = None
        selected_idx = None
        
        for idx, (farm_name, (farm_lat, farm_lng)) in enumerate(coordinates):
            distance = ((farm_lat - clicked_lat) ** 2 + (farm_lng - clicked_lng) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                selected_farm = farm_name
                selected_idx = idx
        
        if min_distance < 0.01:  # Threshold for considering a click as selecting a farm
            st.session_state.selected_farm = selected_farm
            st.session_state.selected_index = selected_idx
    
with col2:
    if st.session_state.selected_farm:
        st.markdown(f"### **{st.session_state.selected_farm}**")
        # Get description from CSV if available, otherwise use fallback
        if df_farms is not None:
            description = df_farms.iloc[st.session_state.selected_index]['Paragraph Synopsis']
            st.markdown(description)
        else:
            st.markdown(farm_descriptions[st.session_state.selected_farm])
    else:
        st.markdown("### Selected Farm Information")
        st.markdown("*Click on a farm marker to view its information*")

st.markdown(
    "Black Owned Centennial Farms are farms that have been owned and operated by the same family for 100 years or more. "
    "These farms have a rich history tied to the broader history of Black Americans in the U.S. "
    "The Black Farmers Network (BFN) works to preserve and promote these farms, supporting the families that own them. "
    "Currently, there are 12 centennial farms in Georgia. Please interact with the map to learn more!"
)