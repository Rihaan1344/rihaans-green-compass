import streamlit as st
import os
from PIL import Image

uploaded_image = st.file_uploader(
    "choose a file",
    type=["jpg", "png", "jpeg"]
)

if uploaded_image is not None:

    st.image(uploaded_image)
    binary_data = uploaded_image.read()
    uploaded_image.seek(0)
    print(uploaded_image.read())

