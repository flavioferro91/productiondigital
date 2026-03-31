import streamlit as st
from datetime import datetime

from menu import show_menu
from utils import append_to_excel, configure_page, get_excel_path, render_live_clock

EXCEL_PACKAGING = get_excel_path("packaging.xlsx")

configure_page("MAPO Controlling - Packaging Produzione")

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

render_live_clock("packaging_produzione_clock")

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
            st.rerun()

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
    rows_to_save = []
    for row in range(st.session_state.rows_pack_prod):
        tipo = st.session_state[f"prod_tipo_{row}"].strip()
        lotto = st.session_state[f"prod_lotto_{row}"].strip()
        n_box = st.session_state[f"prod_box_{row}"]

        if not tipo and not lotto and n_box == 0:
            continue

        if not tipo or not lotto or n_box <= 0:
            st.warning(f"Completa correttamente tipologia, lotto e numero box nella riga {row + 1}.")
            st.stop()

        rows_to_save.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reparto": "Packaging",
                "tipo_prodotto": tipo,
                "lotto": lotto,
                "n_box": n_box,
            }
        )

    if not rows_to_save:
        st.warning("Inserisci almeno una riga valida prima di inviare.")
    else:
        saved_path = None
        for payload in rows_to_save:
            saved_path = append_to_excel(EXCEL_PACKAGING, payload)

        st.success(f"✅ Produzione inviata correttamente in {saved_path.name}!")

st.write("")
st.write("")
