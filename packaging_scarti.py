import streamlit as st
from datetime import datetime
from menu import show_menu
from utils import append_to_excel

# ✅ Percorso Excel OneDrive
EXCEL_PACKAGING = r"C:\Users\fferro\OneDrive - Work\progetto digital production\Excel\packaging.xlsx"

# ✅ CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="MAPO Controlling - Packaging Scarti",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ IMPORTA CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ MENU HAMBURGER
show_menu({
    "HOME": "packaging_home.py",
    "COUNTING SCARTI": "packaging_scarti.py",
    "PRODUZIONE": "packaging_produzione.py",
    "PEDANE": "packaging_pedane.py"
})

# ✅ HEADER IDENTICO ALLA UI
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>P A C K A G I N G &nbsp;&nbsp; scarti</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data + orario
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

# ------------------------------------------------------
# ✅ GESTIONE RIGHE DINAMICHE (max 5)
# ------------------------------------------------------
if "rows_packaging_scarti" not in st.session_state:
    st.session_state.rows_packaging_scarti = 1

# ✅ Bottone aggiungi riga
if st.button("➕ Aggiungi nuova riga di scarto"):
    if st.session_state.rows_packaging_scarti < 5:
        st.session_state.rows_packaging_scarti += 1
    else:
        st.warning("Puoi inserire al massimo 5 linee di scarti.")

# ------------------------------------------------------
# ✅ TABELLA DINAMICA
# ------------------------------------------------------
st.write("")
st.write("### Scarti giornalieri")

for row in range(st.session_state.rows_packaging_scarti):
    
    col_delete, col_tipo, col_plus, col_minus, col_prob = st.columns([1,5,1,1,5])

    # ✅ Icona elimina
    with col_delete:
        if st.button("✖", key=f"del_{row}"):
            if st.session_state.rows_packaging_scarti > 1:
                st.session_state.rows_packaging_scarti -= 1
            st.experimental_rerun()

    # ✅ Tipologia
    with col_tipo:
        st.text_input(f"Tipologia {row+1}", 
                      value="SCROCCO FROZEN CLASSICA 25CM 22X210G" if row == 0 else "",
                      key=f"tipo_{row}")

    # ✅ + verde
    with col_plus:
        st.markdown("<span class='plus-btn'>＋</span>", unsafe_allow_html=True)

    # ✅ – arancione
    with col_minus:
        st.markdown("<span class='minus-btn'>−</span>", unsafe_allow_html=True)

    # ✅ Problematiche
    with col_prob:
        st.text_input("Problematica", key=f"prob_{row}")

st.write("")

# ✅ INVIO DATI A EXCEL
if st.button("INVIA RESOCONTO SCARTI"):
    for row in range(st.session_state.rows_packaging_scarti):
        append_to_excel(EXCEL_PACKAGING, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reparto": "Packaging",
            "tipo": st.session_state[f"tipo_{row}"],
            "problematica": st.session_state[f"prob_{row}"]
        })
    st.success("✅ Resoconto scarti inviato correttamente!")

st.write("")
st.write("")
``