import streamlit as st

from streamlit.components.v1 import html

# Read the HTML file
with open('cafe_map.html', 'r') as file:
    html_content = file.read()

# Display the HTML content in Streamlit
html(html_content, height=800)