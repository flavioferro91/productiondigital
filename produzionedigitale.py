import streamlit as st

# ✅ Configurazione pagina
st.set_page_config(
    page_title="MAPO Controlling",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    reparto = st.selectbox("", ["Impasti", "Packaging", "Formatura"])

    # Sezione addetto
    st.markdown("<div class='excel-box'>ADDETTO CONTROLLING</div>", unsafe_allow_html=True)
    nome = st.text_input("", placeholder="--- inserisci ---")

    # Password
    pw = st.text_input("Inserisci password", type="password")

    # Pulsante ACCEDI
    if st.button("ACCEDI"):
        if pw == "1234":
            st.session_state["user"] = nome
            st.session_state["reparto"] = reparto

            # Redirect in base al reparto
            if reparto == "Packaging":
                st.switch_page("packaging_home.py")
            elif reparto == "Impasti":
                st.switch_page("impasti_home.py")
            elif reparto == "Formatura":
                st.switch_page("formatura_home.py")
        else:
            st.error("Password errata")

# Messaggio benvenuto
if "user" in st.session_state:
    st.markdown(
        f"<p style='color:red; text-align:center; font-size:20px;'><b>BENVENUTO {st.session_state['user'].upper()}, BUON LAVORO! 😊</b></p>",
        unsafe_allow_html=True
    )