import streamlit as st

from streamlit.components.v1 import html

#Creating a title
st.header("Cafes and Desserts in Singapore Map")
st.subheader("A map to show the cafes in Singapore and desserts within 500m proximity of the cafes")

# Read the HTML file
with open('cafe_map.html', 'r') as file:
    html_content = file.read()

with open('searchbar.html', 'r') as file:
    html_bar = file.read()
    
col1, col2 = st.columns(2)
# Display the HTML content in Streamlit
with col1:
     html(html_bar, height = 800)
with col2:
    html(html_content, height=800)