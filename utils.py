import importlib.util
import os
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent


def configure_page(page_title="MAPO Controlling"):
    """Configura la pagina una sola volta per supportare router interno e pagine dirette."""
    if st.session_state.get("_page_configured"):
        return

    st.set_page_config(
        page_title=page_title,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.session_state["_page_configured"] = True


def _candidate_data_dirs():
    env_dir = os.getenv("MAPO_EXCEL_DIR")
    if env_dir:
        yield Path(env_dir).expanduser()

    home = Path.home()
    yield home / "OneDrive - Work" / "progetto digital production" / "Excel"

    cloud_storage = home / "Library" / "CloudStorage"
    if cloud_storage.exists():
        for candidate in cloud_storage.glob("OneDrive*"):
            yield candidate / "progetto digital production" / "Excel"

    yield APP_DIR / "data"


def get_excel_path(filename):
    """Restituisce un percorso scrivibile per i file dati dell'app."""
    for directory in _candidate_data_dirs():
        if directory.exists():
            return directory / filename

    fallback_dir = APP_DIR / "data"
    fallback_dir.mkdir(parents=True, exist_ok=True)
    return fallback_dir / filename


def _concat_rows(existing_df, row_dict):
    return pd.concat([existing_df, pd.DataFrame([row_dict])], ignore_index=True)


def append_to_excel(path, row_dict):
    """Appende una riga a un file Excel, con fallback CSV se Excel non e disponibile."""
    target = Path(path).expanduser()
    if not target.is_absolute():
        target = APP_DIR / target
    target.parent.mkdir(parents=True, exist_ok=True)

    openpyxl_available = importlib.util.find_spec("openpyxl") is not None
    if target.suffix.lower() == ".xlsx" and openpyxl_available:
        try:
            existing_df = pd.read_excel(target) if target.exists() else pd.DataFrame()
        except Exception:
            existing_df = pd.DataFrame()

        df = _concat_rows(existing_df, row_dict)
        df.to_excel(target, index=False)
        return target

    csv_target = target.with_suffix(".csv")
    try:
        existing_df = pd.read_csv(csv_target) if csv_target.exists() else pd.DataFrame()
    except Exception:
        existing_df = pd.DataFrame()

    df = _concat_rows(existing_df, row_dict)
    df.to_csv(csv_target, index=False)
    return csv_target
