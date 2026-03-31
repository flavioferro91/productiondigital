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

EXCEL_IMPASTI = get_excel_path("impasti.xlsx")
TIPOLOGIE_IMPASTI = ["55x25", "25,38x38", "16x28", "25", "31", "58x38", "40"]
PAGE_PREFIX = "impasti_scarti"

configure_page("MAPO Controlling - Impasti Scarti")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_menu(
    {
        "HOME": "impasti_home.py",
        "SCARTI": "impasti_scarti.py",
    }
)


@st.dialog("Conferma inserimento riga")
def confirm_row_dialog(row):
    tipo = st.session_state.get(f"imp_tipo_{row}", "")
    problematica = st.session_state.get(f"imp_prob_{row}", "").strip()
    quantita = st.session_state.get(f"imp_qty_{row}", 0)

    if not tipo or not problematica or quantita <= 0:
        st.warning("Per confermare la riga devi selezionare tipologia, quantità e problematica.")
        if st.button("Chiudi", key=f"{PAGE_PREFIX}_row_invalid_{row}"):
            st.rerun()
        return

    st.write(f"Confermi la riga {row + 1}?")
    st.markdown(f"- Tipologia: **{tipo}**")
    st.markdown(f"- Quantità: **{quantita}**")
    st.markdown(f"- Problematica: **{problematica}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Conferma", key=f"{PAGE_PREFIX}_row_confirm_{row}"):
            st.session_state[f"imp_locked_{row}"] = True
            persist_daily_state()
            st.rerun()
    with col2:
        if st.button("Annulla", key=f"{PAGE_PREFIX}_row_cancel_{row}"):
            st.rerun()


@st.dialog("Conferma invio resoconto")
def confirm_submit_dialog():
    rows_to_save = []
    summary_lines = []

    for row in range(st.session_state.rows_impasti_scarti):
        locked = st.session_state.get(f"imp_locked_{row}", False)
        tipologia = st.session_state.get(f"imp_tipo_{row}", "").strip()
        problematica = st.session_state.get(f"imp_prob_{row}", "").strip()
        quantita = st.session_state.get(f"imp_qty_{row}", 0)

        if not tipologia and not problematica and quantita == 0:
            continue

        if not locked:
            st.warning(f"La riga {row + 1} non e stata confermata con INSERISCI.")
            if st.button("Chiudi", key=f"{PAGE_PREFIX}_submit_not_locked"):
                st.rerun()
            return

        rows_to_save.append(
            {
                "timestamp": current_storage_timestamp(),
                "reparto": "Impasti",
                "tipologia": tipologia,
                "quantita": quantita,
                "problematica": problematica,
            }
        )
        summary_lines.append(f"Riga {row + 1}: {tipologia} | qta {quantita} | {problematica}")

    if not rows_to_save:
        st.warning("Inserisci almeno una riga valida prima di inviare.")
        if st.button("Chiudi", key=f"{PAGE_PREFIX}_submit_empty"):
            st.rerun()
        return

    st.write("Confermi l'invio del resoconto scarti?")
    for line in summary_lines:
        st.markdown(f"- {line}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Conferma invio", key=f"{PAGE_PREFIX}_submit_confirm"):
            saved_path = None
            for payload in rows_to_save:
                saved_path = append_to_excel(EXCEL_IMPASTI, payload)
            st.session_state[f"{PAGE_PREFIX}_last_report"] = summary_lines
            st.session_state[f"{PAGE_PREFIX}_last_saved_file"] = saved_path.name if saved_path else ""
            persist_daily_state()
            st.rerun()
    with col2:
        if st.button("Annulla", key=f"{PAGE_PREFIX}_submit_cancel"):
            st.rerun()


st.markdown(
    """
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>I M P A S T I &nbsp;&nbsp; scarti</span>
</div>
""",
    unsafe_allow_html=True,
)

start_time = st.session_state.get("impasti_home_start_time", "")
end_time = st.session_state.get("impasti_home_end_time", "")
render_live_clock("impasti_scarti_clock", start_time=start_time, end_time=end_time)

if "rows_impasti_scarti" not in st.session_state:
    st.session_state.rows_impasti_scarti = 1

st.write("")

if st.button("Aggiungi nuova riga di scarto"):
    if st.session_state.rows_impasti_scarti < 5:
        st.session_state.rows_impasti_scarti += 1
        persist_daily_state()
        st.rerun()
    else:
        st.warning("Puoi inserire al massimo 5 righe di scarti.")

st.markdown("<div class='page-section-title'>Scarti Impasti</div>", unsafe_allow_html=True)

for row in range(st.session_state.rows_impasti_scarti):
    qty_key = f"imp_qty_{row}"
    locked_key = f"imp_locked_{row}"
    st.session_state.setdefault(qty_key, 0)
    st.session_state.setdefault(locked_key, False)
    locked = st.session_state[locked_key]

    row_class = "row-card row-card-locked" if locked else "row-card"
    st.markdown(f"<div class='{row_class}'>", unsafe_allow_html=True)
    col_x, col_tipo, col_minus, col_count, col_plus, col_prob, col_insert = st.columns([0.8, 3.2, 1, 1.2, 1, 4, 1.8])

    with col_x:
        if st.button("✖", key=f"imp_del_{row}", disabled=locked):
            if st.session_state.rows_impasti_scarti > 1:
                st.session_state.rows_impasti_scarti -= 1
                persist_daily_state()
            st.rerun()

    with col_tipo:
        st.selectbox(
            f"Tipologia {row + 1}",
            [""] + TIPOLOGIE_IMPASTI,
            key=f"imp_tipo_{row}",
            format_func=lambda value: "Seleziona tipologia" if value == "" else value,
            disabled=locked,
        )

    with col_minus:
        if st.button("−", key=f"imp_minus_{row}", disabled=locked):
            if st.session_state[qty_key] > 0:
                st.session_state[qty_key] -= 1
                persist_daily_state()
            st.rerun()

    with col_count:
        st.markdown(f"<div class='counter-box'>{st.session_state[qty_key]}</div>", unsafe_allow_html=True)

    with col_plus:
        if st.button("+", key=f"imp_plus_{row}", disabled=locked):
            st.session_state[qty_key] += 1
            persist_daily_state()
            st.rerun()

    with col_prob:
        st.text_input(
            "Problematica",
            placeholder="Es: consistenza errata / umidita errata",
            key=f"imp_prob_{row}",
            disabled=locked,
        )

    with col_insert:
        label = "CONFERMATO" if locked else "INSERISCI"
        if st.button(label, key=f"imp_insert_{row}", disabled=locked):
            confirm_row_dialog(row)

    st.markdown("</div>", unsafe_allow_html=True)

persist_daily_state()

st.write("")

if st.button("INVIA RESOCONTO SCARTI"):
    confirm_submit_dialog()

confirmed_lines = []
for row in range(st.session_state.rows_impasti_scarti):
    if st.session_state.get(f"imp_locked_{row}", False):
        tipologia = st.session_state.get(f"imp_tipo_{row}", "").strip()
        problematica = st.session_state.get(f"imp_prob_{row}", "").strip()
        quantita = st.session_state.get(f"imp_qty_{row}", 0)
        if tipologia and quantita:
            confirmed_lines.append(f"Riga {row + 1}: {tipologia} | qta {quantita} | {problematica}")

if confirmed_lines:
    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
    st.markdown("### Scarti confermati")
    for line in confirmed_lines:
        st.markdown(f"- {line}")
    st.markdown("</div>", unsafe_allow_html=True)

last_report = st.session_state.get(f"{PAGE_PREFIX}_last_report", [])
last_saved_file = st.session_state.get(f"{PAGE_PREFIX}_last_saved_file", "")
if last_report:
    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
    st.markdown("### Ultimo resoconto inviato")
    for line in last_report:
        st.markdown(f"- {line}")
    if last_saved_file:
        st.markdown(f"**File aggiornato:** {last_saved_file}")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")
