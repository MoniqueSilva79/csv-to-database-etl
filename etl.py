"""ETL: lê CSVs brutos, limpa os dados e carrega em banco relacional."""
import glob
import os
import re

import pandas as pd
from sqlalchemy import create_engine

RAW_DIR = "data/raw"
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///clientes.db")
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def extract() -> pd.DataFrame:
    files = glob.glob(f"{RAW_DIR}/*.csv")
    print(f"[EXTRACT] {len(files)} arquivo(s) encontrado(s)")
    return pd.concat((pd.read_csv(f, dtype=str) for f in files), ignore_index=True)


def parse_money(value) -> float | None:
    if pd.isna(value):
        return None
    value = str(value).replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(value)
    except ValueError:
        return None


def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    df["nome"] = df["nome"].str.title()
    df["email"] = df["email"].str.lower()
    df["uf"] = df["uf"].str.upper()
    df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], dayfirst=True, errors="coerce", format="mixed")
    df["valor_compras"] = df["valor_compras"].map(parse_money)

    valid = df["email"].fillna("").str.match(EMAIL_RE) & df["nome"].notna() & df["data_cadastro"].notna()
    rejected = df[~valid]
    clean = df[valid].drop_duplicates(subset="email", keep="last").copy()
    clean["data_cadastro"] = clean["data_cadastro"].dt.date

    print(f"[TRANSFORM] válidas: {len(clean)} | rejeitadas: {len(rejected)} | "
          f"duplicadas removidas: {valid.sum() - len(clean)}")
    return clean, rejected


def load(df: pd.DataFrame) -> None:
    engine = create_engine(DATABASE_URL)
    df.to_sql("clientes", engine, if_exists="replace", index=False)
    print(f"[LOAD] {len(df)} linhas carregadas em 'clientes' ({DATABASE_URL.split(':')[0]})")


if __name__ == "__main__":
    data = extract()
    clean, rejected = transform(data)
    rejected.to_csv("rejeitados.csv", index=False)
    load(clean)
