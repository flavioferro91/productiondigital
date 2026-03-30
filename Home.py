import streamlit as st

st.set_page_config(layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<div class='title-center'>BENVENUTO IN MAPO Controlling Beta V1</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Seleziona il reparto e inserisci le tue informazioni operatore</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])

with col2:
    st.markdown("<div class='excel-box'>REPARTO</div>", unsafe_allow_html=True)
    reparto = st.selectbox("", ["Impasti", "Packaging"], key="rep")

    st.markdown("<div class='excel-box'>ADDETTO CONTROLLING</div>", unsafe_allow_html=True)
    nome = st.text_input("", placeholder="--- inserisci ---", key="nome")

    password = st.text_input("Inserisci password", type="password")

    if st.button("ACCEDI"):
        if password == "1234":
            st.session_state.user = nome
            st.session_state.reparto = reparto

            if reparto == "Packaging":
                st.switch_page("packaging_home.py")
            elif reparto == "Impasti":
                st.switch_page("impasti_home.py")
        else:
            st.error("Password errata")

if "user" in st.session_state:
    st.markdown(
        f"<p style='color:red;text-align:center;'><b>BENVENUTO {st.session_state.user.upper()}, BUON LAVORO! 😊</b></p>",
        unsafe_allow_html=True
    )
``