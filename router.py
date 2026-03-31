from pathlib import Path
import runpy

import streamlit as st


APP_DIR = Path(__file__).resolve().parent


def navigate(page_filename):
    st.session_state["_target_page"] = page_filename
    st.rerun()


def go_to_login(clear_auth=False):
    if clear_auth:
        for key in [
            "user",
            "reparto",
            "login_password",
            "_target_page",
        ]:
            st.session_state.pop(key, None)
    else:
        st.session_state.pop("_target_page", None)
    st.rerun()


def render_current_page():
    target = st.session_state.get("_target_page")
    if not target:
        return False

    runpy.run_path(str(APP_DIR / target), run_name="__main__")
    st.stop()
    return True
