import streamlit as st
from datetime import datetime

from menu import show_menu
from utils import append_to_excel, configure_page, get_excel_path

EXCEL_FORMATURA = get_excel_path("formatura.xlsx")

configure_page("MAPO Controlling - Formatura Scarti")

# ✅ Importa CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ MENU HAMBURGER
show_menu({
    "HOME": "formatura_home.py",
    "SCARTI": "formatura_scarti.py"
})

# ✅ HEADER stile MAPO
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>F O R M A T U R A &nbsp;&nbsp; scarti</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data + ora
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------------
# ✅ Gestione righe dinamiche (max 5)
# -----------------------------------------------------------
if "rows_formatura_scarti" not in st.session_state:
    st.session_state.rows_formatura_scarti = 1

# ✅ Aggiungi riga
if st.button("➕ Aggiungi nuova riga di scarto"):
    if st.session_state.rows_formatura_scarti < 5:
        st.session_state.rows_formatura_scarti += 1
    else:
        st.warning("Puoi inserire al massimo 5 righe di scarti.")

st.write("### Scarti Formatura")

# -----------------------------------------------------------
# ✅ Tabella dinamica
# -----------------------------------------------------------
for row in range(st.session_state.rows_formatura_scarti):

    col_x, col_tipo, col_plus, col_minus, col_prob = st.columns([1,5,1,1,5])

    # ❌ Bottone elimina riga
    with col_x:
        if st.button("✖", key=f"form_del_{row}"):
            if st.session_state.rows_formatura_scarti > 1:
                st.session_state.rows_formatura_scarti -= 1
                st.experimental_rerun()

    # ✅ Tipologia scarto
    with col_tipo:
        st.text_input(
            f"Tipologia {row+1}",
            placeholder="Es: Scarto formatura / forma non conforme",
            key=f"form_tipo_{row}"
        )

    # ✅ Icona +
    with col_plus:
        st.markdown("<span class='plus-btn'>＋</span>", unsafe_allow_html=True)

    # ✅ Icona –
    with col_minus:
        st.markdown("<span class='minus-btn'>−</span>", unsafe_allow_html=True)

    # ✅ Problematiche
    with col_prob:
        st.text_input(
            "Problematica",
            placeholder="Es: deformazione, rottura, difetto bordo…",
            key=f"form_prob_{row}"
        )

st.write("")
st.write("")

# -----------------------------------------------------------
# ✅ INVIO DATI A EXCEL
# -----------------------------------------------------------
if st.button("✅ INVIA RESOCONTO SCARTI"):
    rows_to_save = []
    for row in range(st.session_state.rows_formatura_scarti):
        tipologia = st.session_state[f"form_tipo_{row}"].strip()
        problematica = st.session_state[f"form_prob_{row}"].strip()

        if not tipologia and not problematica:
            continue

        if not tipologia or not problematica:
            st.warning(f"Completa tipologia e problematica nella riga {row + 1}.")
            st.stop()

        rows_to_save.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reparto": "Formatura",
                "tipologia": tipologia,
                "problematica": problematica,
            }
        )

    if not rows_to_save:
        st.warning("Inserisci almeno una riga valida prima di inviare.")
    else:
        saved_path = None
        for payload in rows_to_save:
            saved_path = append_to_excel(EXCEL_FORMATURA, payload)

        st.success(f"✅ Resoconto scarti inviato correttamente in {saved_path.name}!")

st.write("")
st.write("")
