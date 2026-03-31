import streamlit as st
from router import go_to_login, navigate

def show_menu(pages: dict):
    """Visualizza menu hamburger con login/logout contestuale."""
    if "menu_open" not in st.session_state:
        st.session_state.menu_open = False

    col1, col2 = st.columns([10,1])
    with col2:
        if st.button("☰", key="hamburger"):
            st.session_state.menu_open = not st.session_state.menu_open

    if st.session_state.menu_open:
        st.markdown("<div class='menu-box'>", unsafe_allow_html=True)
        for label, page in pages.items():
            if st.button(label):
                st.session_state.menu_open = False
                navigate(page)
        if "user" in st.session_state:
            if st.button("LOGOUT"):
                st.session_state.menu_open = False
                go_to_login(clear_auth=True)
        else:
            if st.button("LOGIN"):
                st.session_state.menu_open = False
                go_to_login(clear_auth=False)
        st.markdown("</div>", unsafe_allow_html=True)
