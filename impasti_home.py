import streamlit as st
from datetime import datetime
from menu import show_menu
from utils import configure_page

configure_page("MAPO Controlling - Impasti Home")

# ✅ IMPORTA CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ MENU HAMBURGER
show_menu({
    "HOME": "impasti_home.py",
    "SCARTI": "impasti_scarti.py",
})

# ✅ HEADER IDENTICO ALLA UI
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>I M P A S T I &nbsp;&nbsp; home</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data + ora
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ✅ LAYOUT DELLA PAGINA — PULSANTI OPERATIVI
# ------------------------------------------------------------------------------
col1, col2 = st.columns([1,3])

with col1:
    st.markdown("<button class='yellow-btn'>INIZIO LAVORO</button>", unsafe_allow_html=True)
    st.write("")  
    st.markdown("<button class='yellow-btn'>FINE LAVORO</button>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<button class='yellow-btn'>SEGNALA FERMO IMPIANTO</button>", unsafe_allow_html=True)

with col2:
    st.write("")
    st.write("")

# ✅ Margine finale
st.write("")
st.write("")
