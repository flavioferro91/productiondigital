import streamlit as st
from datetime import datetime
from menu import show_menu
from utils import append_to_excel

# ✅ Percorso Excel OneDrive (Impasti)
EXCEL_IMPASTI = r"C:\Users\fferro\OneDrive - Work\progetto digital production\Excel\impasti.xlsx"

# ✅ Configurazione pagina
st.set_page_config(
    page_title="MAPO Controlling - Impasti Scarti",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Importa CSS stile Excel
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Menu hamburger (per Impasti)
show_menu({
    "HOME": "impasti_home.py",
    "SCARTI": "impasti_scarti.py"
})

# ✅ HEADER identico allo stile generale
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>I M P A S T I &nbsp;&nbsp; scarti</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data estesa + ora
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------------------------------
# ✅ Gestione righe dinamiche (max 5)
# -----------------------------------------------------------------------------
if "rows_impasti_scarti" not in st.session_state:
    st.session_state.rows_impasti_scarti = 1

# ✅ Aggiungi riga
if st.button("➕ Aggiungi nuova riga di scarto"):
    if st.session_state.rows_impasti_scarti < 5:
        st.session_state.rows_impasti_scarti += 1
    else:
        st.warning("Puoi inserire al massimo 5 righe di scarti.")

st.write("### Scarti Impasti")

# -----------------------------------------------------------------------------
# ✅ Tabella dinamica
# -----------------------------------------------------------------------------
for row in range(st.session_state.rows_impasti_scarti):

    col_x, col_tipo, col_plus, col_minus, col_prob = st.columns([1,5,1,1,5])

    # ❌ Icona elimina riga
    with col_x:
        if st.button("✖", key=f"imp_del_{row}"):
            if st.session_state.rows_impasti_scarti > 1:
                st.session_state.rows_impasti_scarti -= 1
                st.experimental_rerun()

    # ✅ Tipologia scarto
    with col_tipo:
        st.text_input(
            f"Tipologia {row+1}",
            placeholder="Es: Sfrido pasta - impasto non conforme",
            key=f"imp_tipo_{row}"
        )

    # ✅ + verde (solo icona estetica)
    with col_plus:
        st.markdown("<span class='plus-btn'>＋</span>", unsafe_allow_html=True)

    # ✅ – arancione (solo icona estetica)
    with col_minus:
        st.markdown("<span class='minus-btn'>−</span>", unsafe_allow_html=True)

    # ✅ Problematiche
    with col_prob:
        st.text_input(
            "Problematica",
            placeholder="Es: consistenza errata / umidità errata",
            key=f"imp_prob_{row}"
        )

st.write("")
st.write("")

# -----------------------------------------------------------------------------
# ✅ INVIO A EXCEL OneDrive
# -----------------------------------------------------------------------------
if st.button("✅ INVIA RESOCONTO SCARTI"):
    for row in range(st.session_state.rows_impasti_scarti):
        append_to_excel(EXCEL_IMPASTI, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reparto": "Impasti",
            "tipologia": st.session_state[f"imp_tipo_{row}"],
            "problematica": st.session_state[f"imp_prob_{row}"]
        })

    st.success("✅ Resoconto scarti inviato correttamente!")

st.write("")
st.write("")