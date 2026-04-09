import streamlit as st
from router import navigate, render_current_page
from utils import configure_page

configure_page("MAPO Controlling")
render_current_page()

# ✅ Importa CSS personalizzato
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Titolo in stile MAPO
st.markdown("""
<div class='title-center'>
    BENVENUTO IN MAPO Controlling Beta V1
</div>
""", unsafe_allow_html=True)

# ✅ Sottotitolo
st.markdown("""
<div class='subtitle'>
    Seleziona il reparto e inserisci le informazioni operatore per iniziare la sessione.
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ✅ Form UI identica alla tua
# ------------------------------------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])

with col2:

    # Sezione reparto
    st.markdown("<div class='excel-box'>REPARTO</div>", unsafe_allow_html=True)
    reparto = st.selectbox("", ["Impasti", "Packaging", "Formatura"], key="login_reparto")

    # Sezione addetto
    st.markdown("<div class='excel-box'>ADDETTO CONTROLLING</div>", unsafe_allow_html=True)
    nome = st.text_input("", value="prova", placeholder="--- inserisci ---", key="login_nome")

    # Password
    pw = st.text_input("Inserisci password", type="password", key="login_password")
    st.caption("Credenziali di test: utente `prova`, password `1234`")

    # Pulsante ACCEDI
    if st.button("ACCEDI"):
        if pw.strip() == "1234":
            st.session_state["user"] = nome.strip() or "prova"
            st.session_state["reparto"] = reparto

            # Redirect in base al reparto
            if reparto == "Packaging":
                navigate("packaging_home.py")
            elif reparto == "Impasti":
                navigate("impasti_home.py")
            elif reparto == "Formatura":
                navigate("formatura_home.py")
        else:
            st.error("Password errata")

# Messaggio benvenuto
if "user" in st.session_state:
    st.markdown(
        f"<p style='color:red; text-align:center; font-size:20px;'><b>BENVENUTO {st.session_state['user'].upper()}, BUON LAVORO! 😊</b></p>",
        unsafe_allow_html=True
    )
