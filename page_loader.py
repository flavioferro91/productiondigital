from pathlib import Path
import runpy


APP_DIR = Path(__file__).resolve().parent


def run_page(filename):
    """Esegue una pagina Python del progetto da un wrapper dentro pages/."""
    target = APP_DIR / filename
    runpy.run_path(str(target), run_name="__main__")
