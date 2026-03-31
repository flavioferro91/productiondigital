from pathlib import Path
import runpy

import streamlit as st


APP_DIR = Path(__file__).resolve().parent


def navigate(page_filename):
    st.session_state["_target_page"] = page_filename
    st.rerun()


def render_current_page():
    target = st.session_state.get("_target_page")
    if not target:
        return False

    runpy.run_path(str(APP_DIR / target), run_name="__main__")
    st.stop()
    return True
