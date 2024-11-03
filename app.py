import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Title of the application
st.title("Glacier Comparison in Mountain Ranges")

# Dictionary to map mountain range names to their IDs
mountain_ranges = {
    "Blanca": "1", "Huallanca": "2", "Huayhuash": "3", "Raura": "4", "Huagoruncho": "5",
    "La Viuda": "6", "Central": "7", "Huaytapallana": "8", "Chonta": "9", "Ampato": "10",
    "Vilcabamba": "11", "Urubamba": "12", "Huanzo": "13", "Chila": "14", "Raya": "15",
    "Vilcanota": "16", "Carabaya": "17", "Apolobamba": "18", "Volcanica": "19", "Barroso": "20"
}

# Dropdown list for selecting the mountain range
option = st.selectbox("Choose Mountain Range:", list(mountain_ranges.keys()))

# Base URL for the images
base_url = "https://github.com/Carlos93U/glacier_insight/raw/first-version/data/raw"

# Generate URLs and title dynamically based on selected option
mountain_id = mountain_ranges[option]
glacier_image_url = f"{base_url}/{mountain_id}_{option.replace(' ', '_')}/Glaciers_comparison.png"
histogram_image_url = f"{base_url}/{mountain_id}_{option.replace(' ', '_')}/histograms_comparison.png"
title = f"Mountain Range {option} 1989 - 2020"

# Display the title for glacier comparison
st.subheader(title)
response_glacier = requests.get(glacier_image_url)
glacier_image = Image.open(BytesIO(response_glacier.content))
st.image(glacier_image, caption="Glacier Comparison")

# Display the title for histogram
st.subheader("Histograms 1989 - 2020")
response_histogram = requests.get(histogram_image_url)
histogram_image = Image.open(BytesIO(response_histogram.content))
st.image(histogram_image, caption="Histogram Comparison")
