import streamlit as st

from menu import show_menu
from utils import (
    add_stop_event,
    configure_page,
    current_timestamp,
    init_workday_state,
    persist_daily_state,
    render_live_clock,
    render_workday_summary,
)

PAGE_PREFIX = "impasti_home"

configure_page("MAPO Controlling - Impasti Home")
init_workday_state(PAGE_PREFIX)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_menu(
    {
        "HOME": "impasti_home.py",
        "SCARTI": "impasti_scarti.py",
    }
)


@st.dialog("Conferma operazione")
def confirm_work_action(field_name, label):
    timestamp = current_timestamp()
    st.write(f"Confermi **{label}** alle **{timestamp}**?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Conferma", key=f"{PAGE_PREFIX}_{field_name}_confirm"):
            st.session_state[f"{PAGE_PREFIX}_{field_name}"] = timestamp
            persist_daily_state()
            st.rerun()
    with col2:
        if st.button("Annulla", key=f"{PAGE_PREFIX}_{field_name}_cancel"):
            st.rerun()


@st.dialog("Operazione non disponibile")
def blocked_action_dialog(message):
    st.warning(message)
    if st.button("Chiudi", key=f"{PAGE_PREFIX}_blocked_close"):
        st.rerun()


@st.dialog("Segnala fermo impianto")
def stop_dialog():
    from_time = st.text_input("Da ora", value=current_timestamp(), key=f"{PAGE_PREFIX}_stop_from")
    to_time = st.text_input("A ora", key=f"{PAGE_PREFIX}_stop_to")
    comment = st.text_area("Commento", key=f"{PAGE_PREFIX}_stop_comment")

    if st.button("Invia", key=f"{PAGE_PREFIX}_stop_send"):
        if not from_time.strip() or not to_time.strip():
            st.warning("Compila sia l'ora di inizio sia l'ora di fine.")
            st.stop()
        add_stop_event(PAGE_PREFIX, from_time.strip(), to_time.strip(), comment)
        st.rerun()


start_time = st.session_state.get(f"{PAGE_PREFIX}_start_time", "")
end_time = st.session_state.get(f"{PAGE_PREFIX}_end_time", "")

st.markdown(
    """
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>I M P A S T I &nbsp;&nbsp; home</span>
</div>
""",
    unsafe_allow_html=True,
)

render_live_clock("impasti_home_clock", start_time=start_time, end_time=end_time)

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("INIZIO LAVORO", key=f"{PAGE_PREFIX}_start_button", disabled=bool(start_time)):
        confirm_work_action("start_time", "inizio lavoro")

    st.write("")

    if st.button("FINE LAVORO", key=f"{PAGE_PREFIX}_end_button", disabled=bool(end_time)):
        if not start_time:
            blocked_action_dialog("Non e stato dichiarato l'inizio lavoro. Il suo utilizzo e inibito.")
        else:
            confirm_work_action("end_time", "fine lavoro")

    st.write("")

    if st.button("SEGNALA FERMO IMPIANTO", key=f"{PAGE_PREFIX}_stop_button"):
        stop_dialog()

with col2:
    render_workday_summary(PAGE_PREFIX, "Fermi impianto")

st.write("")
st.write("")
persist_daily_state()
