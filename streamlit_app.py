import streamlit as st
import requests
from streamlit.components.v1 import html

#Creating a title
st.header("Cafes and Desserts in Singapore Map")
st.subheader("A map to show the cafes in Singapore and desserts within 500m proximity of the cafes")

#Create the columns to display content
col1, col2 = st.columns(2)

# Read the HTML file
with open('cafe_map.html', 'r') as file:
    folium_map_html = file.read()

# Render the search input
with col1:
    search_input = st.text_input("Search for a location")
    # Perform AJAX request when the search input is changed
    if search_input:
        autocomplete_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={search_input}&key=AIzaSyC4Ua2RlccldtqrPOmUzj_kgV7baVgcDM8"
        response = requests.get(autocomplete_url)
        data = response.json()

        # Extract the autocomplete suggestions from the response
        if data['status'] == 'OK':
            suggestions = [prediction['description'] for prediction in data['predictions']]
            st.write("Autocomplete Suggestions:", suggestions)

    # Perform AJAX request when the search button is clicked
    if st.button("Search"):
        # Get the selected location coordinates using Google Geocoding API
        geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={search_input}&key=AIzaSyC4Ua2RlccldtqrPOmUzj_kgV7baVgcDM8"
        response = requests.get(geocoding_url)
        data = response.json()

        # Extract the latitude and longitude from the response
        if data['status'] == 'OK':
            new_latitude = data['results'][0]['geometry']['location']['lat']
            new_longitude = data['results'][0]['geometry']['location']['lng']

            folium_map_html = folium_map_html.replace('1.3114516', str(new_latitude))
            folium_map_html = folium_map_html.replace('103.8561608', str(new_longitude))
            with open('folium_map.html', 'w') as file:
                file.write(folium_map_html)
            st.success("Map updated successfully")


with col2:
    html(folium_map_html, height=800)