import streamlit as st
from datetime import datetime
from menu import show_menu
from utils import append_to_excel

# ✅ Percorso file Excel OneDrive
EXCEL_PACKAGING = r"C:\Users\fferro\OneDrive - Work\progetto digital production\Excel\packaging.xlsx"

# ✅ Configurazione pagina Streamlit
st.set_page_config(
    page_title="MAPO Controlling - Packaging Produzione",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Importa CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ MENU HAMBURGER
show_menu({
    "HOME": "packaging_home.py",
    "COUNTING SCARTI": "packaging_scarti.py",
    "PRODUZIONE": "packaging_produzione.py",
    "PEDANE": "packaging_pedane.py"
})

# ✅ HEADER pagina
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>P A C K A G I N G &nbsp;&nbsp; produzione</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data + orario
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

st.write("")

# -------------------------------------------------------------
# ✅ GESTIONE RIGHE DINAMICHE (max 5)
# -------------------------------------------------------------
if "rows_pack_prod" not in st.session_state:
    st.session_state.rows_pack_prod = 1

# ✅ Bottone "Aggiungi riga"
if st.button("➕ Aggiungi nuova riga di produzione"):
    if st.session_state.rows_pack_prod < 5:
        st.session_state.rows_pack_prod += 1
    else:
        st.warning("Puoi inserire al massimo 5 righe di produzione.")

# -------------------------------------------------------------
# ✅ TABELLA DINAMICA
# -------------------------------------------------------------
st.write("### Inserimento produzione giornaliera")

for row in range(st.session_state.rows_pack_prod):
    
    col_x, col_tipo, col_lotto, col_box = st.columns([1,4,3,2])

    # ✅ Icona elimina riga
    with col_x:
        if st.button("✖", key=f"prod_del_{row}"):
            if st.session_state.rows_pack_prod > 1:
                st.session_state.rows_pack_prod -= 1
            st.experimental_rerun()

    # ✅ Tipologia
    with col_tipo:
        st.text_input(f"Tipologia {row+1}", 
                      placeholder="Es: CLASSICA 25CM 22X210G",
                      key=f"prod_tipo_{row}")

    # ✅ Lotto
    with col_lotto:
        st.text_input(f"Lotto {row+1}",
                      placeholder="Es: L240320",
                      key=f"prod_lotto_{row}")

    # ✅ Numero box
    with col_box:
        st.number_input(f"N° box {row+1}", min_value=0, key=f"prod_box_{row}")

st.write("")
st.write("")

# -------------------------------------------------------------
# ✅ INVIO PRODUZIONE A FILE EXCEL
# -------------------------------------------------------------
if st.button("✅ INVIA PRODUZIONE"):
    for row in range(st.session_state.rows_pack_prod):
        append_to_excel(EXCEL_PACKAGING, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reparto": "Packaging",
            "tipo_prodotto": st.session_state[f"prod_tipo_{row}"],
            "lotto": st.session_state[f"prod_lotto_{row}"],
            "n_box": st.session_state[f"prod_box_{row}"]
        })

    st.success("✅ Produzione inviata correttamente!")

st.write("")
st.write("")
