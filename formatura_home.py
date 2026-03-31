import streamlit as st
from datetime import datetime

from menu import show_menu
from utils import configure_page

configure_page("MAPO Controlling - Formatura Home")

# ✅ Importa CSS stile Excel
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Menu hamburger
show_menu({
    "HOME": "formatura_home.py",
    "SCARTI": "formatura_scarti.py"
})

# ✅ HEADER identico allo stile generale
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>F O R M A T U R A &nbsp;&nbsp; home</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data estesa + ora
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("<button class='yellow-btn'>INIZIO LAVORO</button>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<button class='yellow-btn'>FINE LAVORO</button>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<button class='yellow-btn'>SEGNALA FERMO LINEA</button>", unsafe_allow_html=True)

with col2:
    st.write("")
    st.write("")

st.write("")
st.write("")
