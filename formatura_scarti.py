import streamlit as st

from menu import show_menu
from utils import (
    append_to_excel,
    configure_page,
    current_storage_timestamp,
    get_excel_path,
    persist_daily_state,
    render_live_clock,
)

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

render_live_clock("formatura_scarti_clock")

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
        persist_daily_state()
    else:
        st.warning("Puoi inserire al massimo 5 righe di scarti.")

st.markdown("<div class='page-section-title'>Scarti Formatura</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# ✅ Tabella dinamica
# -----------------------------------------------------------
for row in range(st.session_state.rows_formatura_scarti):
    qty_key = f"form_qty_{row}"
    st.session_state.setdefault(qty_key, 0)
    st.markdown("<div class='row-card'>", unsafe_allow_html=True)
    col_x, col_tipo, col_insert, col_count, col_prob = st.columns([1,5,2,1.5,5])

    # ❌ Bottone elimina riga
    with col_x:
        if st.button("✖", key=f"form_del_{row}"):
            if st.session_state.rows_formatura_scarti > 1:
                st.session_state.rows_formatura_scarti -= 1
                persist_daily_state()
                st.rerun()

    # ✅ Tipologia scarto
    with col_tipo:
        st.text_input(
            f"Tipologia {row+1}",
            placeholder="Es: Scarto formatura / forma non conforme",
            key=f"form_tipo_{row}"
        )

    # ✅ Icona +
    with col_insert:
        if st.button("INSERISCI", key=f"form_insert_{row}"):
            st.session_state[qty_key] += 1
            persist_daily_state()
            st.rerun()

    with col_count:
        st.markdown(f"<div class='counter-box'>{st.session_state[qty_key]}</div>", unsafe_allow_html=True)

    # ✅ Problematiche
    with col_prob:
        st.text_input(
            "Problematica",
            placeholder="Es: deformazione, rottura, difetto bordo…",
            key=f"form_prob_{row}"
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")
persist_daily_state()

# -----------------------------------------------------------
# ✅ INVIO DATI A EXCEL
# -----------------------------------------------------------
if st.button("✅ INVIA RESOCONTO SCARTI"):
    rows_to_save = []
    for row in range(st.session_state.rows_formatura_scarti):
        qty_key = f"form_qty_{row}"
        tipologia = st.session_state[f"form_tipo_{row}"].strip()
        problematica = st.session_state[f"form_prob_{row}"].strip()
        quantita = st.session_state.get(qty_key, 0)
        if not tipologia and not problematica and quantita == 0:
            continue

        if not tipologia or not problematica or quantita <= 0:
            st.warning(f"Completa tipologia, quantità e problematica nella riga {row + 1}.")
            st.stop()

        rows_to_save.append(
            {
                "timestamp": current_storage_timestamp(),
                "reparto": "Formatura",
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
            saved_path = append_to_excel(EXCEL_FORMATURA, payload)

        st.success(f"✅ Resoconto scarti inviato correttamente in {saved_path.name}!")

st.write("")
st.write("")
