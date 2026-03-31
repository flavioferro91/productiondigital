import streamlit as st
from router import go_to_login, navigate

def show_menu(pages: dict):
    """Visualizza un menu compatto, leggibile e ancorato al pulsante hamburger."""
    col1, col2 = st.columns([10, 1])
    with col2:
        with st.popover("☰", use_container_width=True):
            st.markdown("### Navigazione")
            for label, page in pages.items():
                if st.button(label, key=f"menu_{label}_{page}", use_container_width=True):
                    navigate(page)
            if "user" in st.session_state:
                if st.button("Logout", key="menu_logout", use_container_width=True):
                    go_to_login(clear_auth=True)
            else:
                if st.button("Login", key="menu_login", use_container_width=True):
                    go_to_login(clear_auth=False)
