import streamlit as st
from datetime import datetime

from menu import show_menu
from utils import append_to_excel, configure_page, get_excel_path

EXCEL_PACKAGING = get_excel_path("packaging.xlsx")

configure_page("MAPO Controlling - Packaging Scarti")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_menu(
    {
        "HOME": "packaging_home.py",
        "COUNTING SCARTI": "packaging_scarti.py",
        "PRODUZIONE": "packaging_produzione.py",
        "PEDANE": "packaging_pedane.py",
    }
)

st.markdown(
    """
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>P A C K A G I N G &nbsp;&nbsp; scarti</span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='excel-box'>Data estesa di oggi + orario con secondi</div>",
    unsafe_allow_html=True,
)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(
    f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>",
    unsafe_allow_html=True,
)

if "rows_packaging_scarti" not in st.session_state:
    st.session_state.rows_packaging_scarti = 1

if st.button("➕ Aggiungi nuova riga di scarto"):
    if st.session_state.rows_packaging_scarti < 5:
        st.session_state.rows_packaging_scarti += 1
    else:
        st.warning("Puoi inserire al massimo 5 linee di scarti.")

st.write("")
st.write("### Scarti giornalieri")

for row in range(st.session_state.rows_packaging_scarti):
    col_delete, col_tipo, col_plus, col_minus, col_prob = st.columns([1, 5, 1, 1, 5])

    with col_delete:
        if st.button("✖", key=f"del_{row}"):
            if st.session_state.rows_packaging_scarti > 1:
                st.session_state.rows_packaging_scarti -= 1
            st.rerun()

    with col_tipo:
        st.text_input(
            f"Tipologia {row + 1}",
            value="SCROCCO FROZEN CLASSICA 25CM 22X210G" if row == 0 else "",
            key=f"tipo_{row}",
        )

    with col_plus:
        st.markdown("<span class='plus-btn'>＋</span>", unsafe_allow_html=True)

    with col_minus:
        st.markdown("<span class='minus-btn'>−</span>", unsafe_allow_html=True)

    with col_prob:
        st.text_input("Problematica", key=f"prob_{row}")

st.write("")

if st.button("INVIA RESOCONTO SCARTI"):
    rows_to_save = []
    for row in range(st.session_state.rows_packaging_scarti):
        tipo = st.session_state[f"tipo_{row}"].strip()
        problematica = st.session_state[f"prob_{row}"].strip()

        if not tipo and not problematica:
            continue

        if not tipo or not problematica:
            st.warning(f"Completa tipologia e problematica nella riga {row + 1}.")
            st.stop()

        rows_to_save.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reparto": "Packaging",
                "tipo": tipo,
                "problematica": problematica,
            }
        )

    if not rows_to_save:
        st.warning("Inserisci almeno una riga valida prima di inviare.")
    else:
        saved_path = None
        for payload in rows_to_save:
            saved_path = append_to_excel(EXCEL_PACKAGING, payload)

        st.success(f"✅ Resoconto scarti inviato correttamente in {saved_path.name}")

st.write("")
st.write("")
