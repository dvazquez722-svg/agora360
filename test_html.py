import streamlit as st

st.set_page_config(layout="wide")

html = """
<div style="background:red;padding:20px;border-radius:10px;">
<h1 style="color:white;">FUNCIONA</h1>
<p style="color:white;">Esto es una prueba.</p>
</div>
"""

st.markdown(html, unsafe_allow_html=True)