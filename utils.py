import importlib.util
import json
import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

APP_DIR = Path(__file__).resolve().parent
STATE_FILE = APP_DIR / "data" / "daily_state.json"
PERSIST_PREFIXES = (
    "rows_",
    "imp_",
    "pack_",
    "form_",
    "impasti_",
    "packaging_",
    "formatura_",
)


def configure_page(page_title="MAPO Controlling"):
    """Configura la pagina una sola volta per supportare router interno e pagine dirette."""
    if st.session_state.get("_page_configured"):
        return

    st.set_page_config(
        page_title=page_title,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    load_daily_state()
    st.session_state["_page_configured"] = True


def current_timestamp():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def current_storage_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_display_timestamp(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        return None


def current_day_key():
    return datetime.now().strftime("%Y-%m-%d")


def render_live_clock(element_id, start_time="", end_time=""):
    start_dt = parse_display_timestamp(start_time)
    end_dt = parse_display_timestamp(end_time)
    start_iso = start_dt.isoformat() if start_dt else ""
    end_iso = end_dt.isoformat() if end_dt else ""
    elapsed_label = "Durata totale" if end_iso else "Cronometro lavoro"
    safe_start_time = start_time or "--:--:--"
    clock_id = f"{element_id}_clock"
    elapsed_id = f"{element_id}_elapsed"
    html(
        f"""
        <style>
          .clock-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            font-family: Calibri, sans-serif;
          }}
          .clock-card {{
            background: rgba(255,255,255,0.06);
            border: 1px solid #2c2c2c;
            border-radius: 16px;
            padding: 14px 16px;
            color: #ffffff;
            box-shadow: 0 14px 24px rgba(0,0,0,0.22);
          }}
          .clock-card small {{
            display: block;
            color: #d4d4d4;
            font-size: 12px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
          }}
          .clock-card strong {{
            display: block;
            color: #ffffff;
            font-size: 24px;
            line-height: 1.2;
          }}
        </style>
        <div class="clock-grid">
          <div class="clock-card">
            <small>Data e ora</small>
            <strong id="{clock_id}"></strong>
          </div>
          <div class="clock-card">
            <small>Inizio lavoro</small>
            <strong>{safe_start_time}</strong>
          </div>
          <div class="clock-card">
            <small>{elapsed_label}</small>
            <strong id="{elapsed_id}">00:00:00</strong>
          </div>
        </div>
        <script>
          const target = document.getElementById("{clock_id}");
          const elapsedTarget = document.getElementById("{elapsed_id}");
          const startIso = "{start_iso}";
          const endIso = "{end_iso}";
          function pad(value) {{
            return String(value).padStart(2, "0");
          }}
          function formatDuration(totalSeconds) {{
            const seconds = Math.max(0, totalSeconds);
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = seconds % 60;
            return [pad(hours), pad(minutes), pad(secs)].join(":");
          }}
          function updateClock() {{
            const now = new Date();
            const formatted = [
              pad(now.getDate()),
              pad(now.getMonth() + 1),
              now.getFullYear()
            ].join("/") + " " + [
              pad(now.getHours()),
              pad(now.getMinutes()),
              pad(now.getSeconds())
            ].join(":");
            if (target) target.textContent = formatted;
            if (elapsedTarget) {{
              if (!startIso) {{
                elapsedTarget.textContent = "00:00:00";
              }} else {{
                const start = new Date(startIso);
                const end = endIso ? new Date(endIso) : now;
                const diff = Math.floor((end.getTime() - start.getTime()) / 1000);
                elapsedTarget.textContent = formatDuration(diff);
              }}
            }}
          }}
          updateClock();
          setInterval(updateClock, 1000);
        </script>
        """,
        height=120,
    )


def _read_state_file():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_state_file(payload):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def _is_persistable_key(key):
    return any(key.startswith(prefix) for prefix in PERSIST_PREFIXES)


def load_daily_state():
    day_key = current_day_key()
    if st.session_state.get("_daily_state_loaded_for") == day_key:
        return

    stored_state = _read_state_file()
    day_state = stored_state.get(day_key, {})
    for key, value in day_state.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.session_state["_daily_state_loaded_for"] = day_key


def persist_daily_state():
    day_key = current_day_key()
    stored_state = _read_state_file()
    snapshot = {
        key: value
        for key, value in st.session_state.items()
        if _is_persistable_key(key)
    }
    stored_state[day_key] = snapshot

    for existing_day in list(stored_state.keys()):
        if existing_day != day_key:
            del stored_state[existing_day]

    _write_state_file(stored_state)


def init_workday_state(prefix):
    st.session_state.setdefault(f"{prefix}_start_time", "")
    st.session_state.setdefault(f"{prefix}_end_time", "")
    st.session_state.setdefault(f"{prefix}_stops", [])
    persist_daily_state()


def add_stop_event(prefix, from_time, to_time, comment):
    stop_event = {
        "from_time": from_time,
        "to_time": to_time,
        "comment": comment.strip(),
        "created_at": current_timestamp(),
    }
    st.session_state[f"{prefix}_stops"] = [stop_event, *st.session_state[f"{prefix}_stops"][:4]]
    persist_daily_state()


def render_workday_summary(prefix, stop_title):
    start_time = st.session_state.get(f"{prefix}_start_time", "")
    end_time = st.session_state.get(f"{prefix}_end_time", "")
    stops = st.session_state.get(f"{prefix}_stops", [])

    st.markdown("<div class='status-card'>", unsafe_allow_html=True)
    st.markdown("### Stato turno")
    st.markdown(f"**Inizio lavoro:** {start_time or '--:--:--'}")
    st.markdown(f"**Fine lavoro:** {end_time or '--:--:--'}")
    st.markdown(f"**{stop_title}:** {len(stops)}")
    if stops:
        for stop in stops:
            st.markdown(
                f"- {stop['from_time']} -> {stop['to_time']} | {stop['comment'] or 'Nessun commento'}"
            )
    st.markdown("</div>", unsafe_allow_html=True)


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
