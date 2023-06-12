import streamlit as st

from streamlit.components.v1 import html

st.header("Cafes and Desserts in Singapore Map")
st.subheader("A map to show the cafes in Singapore and desserts within 500m proximity of the cafes")

# Read the HTML file
with open('cafe_map.html', 'r') as file:
    html_content = file.read()

# Display the HTML content in Streamlit
with st.container():
    html(html_content, height=800)