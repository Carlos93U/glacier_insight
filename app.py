import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Título de la aplicación
st.title("Comparación de Glaciares en Cordilleras")

# Lista desplegable para seleccionar la cordillera
option = st.selectbox("Seleccione la cordillera:", ["Blanca", "Huallanca"])

# Definición de las rutas de las imágenes según la selección del usuario
base_url = "https://github.com/Carlos93U/glacier_insight/raw/first-version/data/raw"
if option == "Blanca":
    glacier_image_url = f"{base_url}/1_Blanca/Glaciers_comparison.png"
    histogram_image_url = f"{base_url}/1_Blanca/histograms_comparison.png"
    title = "Cordillera Blanca 1989 - 2020"
else:
    glacier_image_url = f"{base_url}/2_Huallanca/Glaciers_comparison.png"
    histogram_image_url = f"{base_url}/2_Huallanca/histograms_comparison.png"
    title = "Cordillera Huallanca 1989 - 2020"

# Mostrar el título para la comparación de glaciares
st.subheader(title)
response_glacier = requests.get(glacier_image_url)
glacier_image = Image.open(BytesIO(response_glacier.content))
st.image(glacier_image, caption="Comparación de Glaciares")

# Mostrar el título para el histograma
st.subheader("Histogramas 1989 - 2020")
response_histogram = requests.get(histogram_image_url)
histogram_image = Image.open(BytesIO(response_histogram.content))
st.image(histogram_image, caption="Comparación de Histogramas")
