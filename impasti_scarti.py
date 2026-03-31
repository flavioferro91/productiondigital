import streamlit as st

from menu import show_menu
from utils import (
    append_to_excel,
    configure_page,
    current_storage_timestamp,
    get_excel_path,
    render_live_clock,
)

EXCEL_IMPASTI = get_excel_path("impasti.xlsx")
TIPOLOGIE_IMPASTI = ["55x25", "25,38x38", "16x28", "25", "31", "58x38", "40"]

configure_page("MAPO Controlling - Impasti Scarti")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_menu(
    {
        "HOME": "impasti_home.py",
        "SCARTI": "impasti_scarti.py",
    }
)

st.markdown(
    """
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>I M P A S T I &nbsp;&nbsp; scarti</span>
</div>
""",
    unsafe_allow_html=True,
)

render_live_clock("impasti_scarti_clock")

if "rows_impasti_scarti" not in st.session_state:
    st.session_state.rows_impasti_scarti = 1

st.write("")

if st.button("➕ Aggiungi nuova riga di scarto"):
    if st.session_state.rows_impasti_scarti < 5:
        st.session_state.rows_impasti_scarti += 1
        st.rerun()
    else:
        st.warning("Puoi inserire al massimo 5 righe di scarti.")

st.write("### Scarti Impasti")

for row in range(st.session_state.rows_impasti_scarti):
    qty_key = f"imp_qty_{row}"
    st.session_state.setdefault(qty_key, 0)

    col_x, col_tipo, col_plus, col_count, col_minus, col_prob = st.columns([1, 4, 1, 1, 1, 5])

    with col_x:
        if st.button("✖", key=f"imp_del_{row}"):
            if st.session_state.rows_impasti_scarti > 1:
                st.session_state.rows_impasti_scarti -= 1
            st.rerun()

    with col_tipo:
        st.selectbox(
            f"Tipologia {row + 1}",
            [""] + TIPOLOGIE_IMPASTI,
            key=f"imp_tipo_{row}",
            format_func=lambda value: "Seleziona tipologia" if value == "" else value,
        )

    with col_plus:
        if st.button("＋", key=f"imp_plus_{row}"):
            st.session_state[qty_key] += 1
            st.rerun()

    with col_count:
        st.markdown(f"<div class='counter-box'>{st.session_state[qty_key]}</div>", unsafe_allow_html=True)

    with col_minus:
        if st.button("−", key=f"imp_minus_{row}"):
            if st.session_state[qty_key] > 0:
                st.session_state[qty_key] -= 1
            st.rerun()

    with col_prob:
        st.text_input(
            "Problematica",
            placeholder="Es: consistenza errata / umidità errata",
            key=f"imp_prob_{row}",
        )

st.write("")
st.write("")

if st.button("✅ INVIA RESOCONTO SCARTI"):
    rows_to_save = []
    for row in range(st.session_state.rows_impasti_scarti):
        tipologia = st.session_state.get(f"imp_tipo_{row}", "").strip()
        problematica = st.session_state.get(f"imp_prob_{row}", "").strip()
        quantita = st.session_state.get(f"imp_qty_{row}", 0)

        if not tipologia and not problematica and quantita == 0:
            continue

        if not tipologia or not problematica or quantita <= 0:
            st.warning(f"Completa tipologia, quantità e problematica nella riga {row + 1}.")
            st.stop()

        rows_to_save.append(
            {
                "timestamp": current_storage_timestamp(),
                "reparto": "Impasti",
                "tipologia": tipologia,
                "quantita": quantita,
                "problematica": problematica,
            }
        )

    if not rows_to_save:
        st.warning("Inserisci almeno una riga valida prima di inviare.")
    else:
        saved_path = None
        for payload in rows_to_save:
            saved_path = append_to_excel(EXCEL_IMPASTI, payload)

        st.success(f"✅ Resoconto scarti inviato correttamente in {saved_path.name}!")

st.write("")
st.write("")
