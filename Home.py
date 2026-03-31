import streamlit as st
from router import navigate, render_current_page
from utils import configure_page

configure_page("MAPO Controlling")
render_current_page()

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    "<div class='title-center'>BENVENUTO IN MAPO Controlling Beta V1</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='subtitle'>Seleziona il reparto e inserisci le informazioni operatore per iniziare la sessione.</div>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.markdown("<div class='excel-box'>REPARTO</div>", unsafe_allow_html=True)
    reparto = st.selectbox("", ["Impasti", "Packaging", "Formatura"], key="rep")

    st.markdown("<div class='excel-box'>ADDETTO CONTROLLING</div>", unsafe_allow_html=True)
    nome = st.text_input("", value="prova", placeholder="--- inserisci ---", key="nome")

    password = st.text_input("Inserisci password", type="password")
    st.caption("Credenziali di test: utente `prova`, password `1234`")

    if st.button("ACCEDI"):
        if password.strip() == "1234":
            st.session_state["user"] = nome.strip()
            st.session_state["reparto"] = reparto

            if reparto == "Packaging":
                navigate("packaging_home.py")
            elif reparto == "Impasti":
                navigate("impasti_home.py")
            elif reparto == "Formatura":
                navigate("formatura_home.py")
        else:
            st.error("Password errata")

if "user" in st.session_state and st.session_state["user"]:
    st.markdown(
        f"<p style='color:red;text-align:center;'><b>BENVENUTO {st.session_state['user'].upper()}, BUON LAVORO!</b></p>",
        unsafe_allow_html=True,
    )
