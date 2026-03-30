import pandas as pd

def append_to_excel(path, row_dict):
    """Scrive una riga nel file Excel dedicato."""
    try:
        old = pd.read_excel(path)
        df = pd.concat([old, pd.DataFrame([row_dict])], ignore_index=True)
    except:
        df = pd.DataFrame([row_dict])

    df.to_excel(path, index=False)