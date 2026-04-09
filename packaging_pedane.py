import streamlit as st
from datetime import datetime
from menu import show_menu
from utils import append_to_excel

# ✅ Percorso file Excel OneDrive
EXCEL_PEDANE = r"C:\Users\fferro\OneDrive - Work\progetto digital production\Excel\pedane packaging.xlsx"

# ✅ Configurazione pagina
st.set_page_config(
    page_title="MAPO Controlling - Packaging Pedane",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Carica CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ✅ Menu hamburger
show_menu({
    "HOME": "packaging_home.py",
    "COUNTING SCARTI": "packaging_scarti.py",
    "PRODUZIONE": "packaging_produzione.py",
    "PEDANE": "packaging_pedane.py"
})

# ✅ Header
st.markdown("""
<div class='title-center'>
    MAPO controlling Beta V1<br>
    <span style='font-size:16px; letter-spacing:4px;'>P A C K A G I N G &nbsp;&nbsp; pedane</span>
</div>
""", unsafe_allow_html=True)

# ✅ Data e ora
st.markdown("<div class='excel-box'>Data estesa di oggi + orario con secondi</div>", unsafe_allow_html=True)
now = datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
st.markdown(f"<p style='text-align:center; font-size:20px;'><b>{now}</b></p>", unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------------------------------
# ✅ Gestione righe dinamiche (max 5 pedane)
# -----------------------------------------------------------------------------
if "rows_pedane" not in st.session_state:
    st.session_state.rows_pedane = 1

if st.button("➕ Aggiungi pedana"):
    if st.session_state.rows_pedane < 5:
        st.session_state.rows_pedane += 1
    else:
        st.warning("Puoi inserire al massimo 5 pedane.")

st.write("### Composizione pedane")

# -----------------------------------------------------------------------------
# ✅ Tabella dinamica
# -----------------------------------------------------------------------------
for row in range(st.session_state.rows_pedane):

    col_x, col_tipo, col_boxped, col_comp, col_tot = st.columns([1,4,2,5,2])

    # ❌ Pulsante elimina
    with col_x:
        if st.button("✖", key=f"ped_del_{row}"):
            if st.session_state.rows_pedane > 1:
                st.session_state.rows_pedane -= 1
                st.experimental_rerun()

    # ✅ Tipologia
    with col_tipo:
        st.text_input(f"Tipologia {row+1}",
                      placeholder="Es: CLASSICA 25CM 22X210G",
                      key=f"ped_tipo_{row}")

    # ✅ Box per pedana
    with col_boxped:
        st.number_input(f"box/ped {row+1}", min_value=0, key=f"ped_box_{row}")

    # ✅ Composizione pedane (lista)
    with col_comp:
        st.text_area(f"Composizione pedana {row+1}",
                     placeholder="Es: 11-11-11-11",
                     key=f"ped_comp_{row}")

    # ✅ Calcolo automatico del totale (somma numeri separati da -)
    with col_tot:
        comp = st.session_state[f"ped_comp_{row}"]
        try:
            tot = sum(int(x) for x in comp.replace(" ", "").split("-") if x.isdigit())
        except:
            tot = 0

        st.number_input("TOT", value=tot, key=f"ped_tot_{row}", disabled=True)

st.write("")

# -----------------------------------------------------------------------------
# ✅ INVIO DELLE PEDANE A EXCEL
# -----------------------------------------------------------------------------
if st.button("✅ CONFERMA PROJECT STACKING"):
    for row in range(st.session_state.rows_pedane):
        append_to_excel(EXCEL_PEDANE, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reparto": "Packaging",
            "tipologia": st.session_state[f"ped_tipo_{row}"],
            "box_per_pedana": st.session_state[f"ped_box_{row}"],
            "composizione": st.session_state[f"ped_comp_{row}"],
            "totale": st.session_state[f"ped_tot_{row}"]
        })
    st.success("✅ Pedane inviate correttamente!")

st.write("")
st.write("")