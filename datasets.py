"""Transparent exploratory analysis of imported engineering observations.

No model is trained and no fabricated dataset is presented as field measurements.
"""
from pathlib import Path
import io
import numpy as np
import pandas as pd

MAX_BYTES = 12 * 1024 * 1024
MAX_ROWS = 200_000

def load_table(content: bytes, filename: str) -> pd.DataFrame:
    if not content or len(content) > MAX_BYTES:
        raise ValueError('Fichier vide ou supérieur à 12 Mo.')
    suffix = Path(filename).suffix.lower()
    if suffix == '.csv':
        try:
            df = pd.read_csv(io.BytesIO(content), sep=None, engine='python')
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(content), sep=None, engine='python', encoding='latin-1')
    elif suffix == '.xlsx':
        df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
    else:
        raise ValueError('Seuls les fichiers CSV et XLSX sont acceptés.')
    if len(df) > MAX_ROWS or len(df.columns) > 150:
        raise ValueError('Limite : 200 000 lignes et 150 colonnes.')
    if df.empty:
        raise ValueError('Le tableau ne contient aucune observation.')
    return df

def audit(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        'variable': [str(c) for c in df.columns],
        'type': [str(df[c].dtype) for c in df.columns],
        'effectif': [int(df[c].notna().sum()) for c in df.columns],
        'manquants': [int(df[c].isna().sum()) for c in df.columns],
        'manquants_pct': [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        'uniques': [int(df[c].nunique(dropna=True)) for c in df.columns]
    })

def numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include='number').replace([np.inf, -np.inf], np.nan)
    if numeric.empty:
        return pd.DataFrame()
    d = numeric.describe(percentiles=[.05, .25, .5, .75, .95]).T
    d['missing'] = numeric.isna().sum()
    d['cv'] = (d['std'] / d['mean'].abs().replace(0, np.nan))
    return d

def linear_fit(df: pd.DataFrame, x: str, y: str):
    if x == y:
        raise ValueError('Choisissez deux variables différentes.')
    pair = df[[x,y]].apply(pd.to_numeric, errors='coerce').replace([np.inf, -np.inf], np.nan).dropna()
    if len(pair) < 4 or pair[x].nunique() < 2:
        raise ValueError('Au moins quatre couples complets et deux valeurs X distinctes sont requis.')
    a,b = np.polyfit(pair[x].to_numpy(float), pair[y].to_numpy(float), 1)
    pred = a * pair[x].to_numpy(float) + b
    ss_res = float(np.sum((pair[y].to_numpy(float)-pred)**2))
    ss_tot = float(np.sum((pair[y].to_numpy(float)-pair[y].mean())**2))
    r2 = 1 - ss_res/ss_tot if ss_tot else float('nan')
    return {'pente':float(a), 'interception':float(b), 'r2':r2, 'n':len(pair)}, pair
