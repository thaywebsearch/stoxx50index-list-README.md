import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

URL_PRIMARY = "https://www.stoxx.com/index-details?symbol=SX5E"
URL_FALLBACK = "https://www.investing.com/indices/stoxx-50-components"

# ---------------------------------------------------------
# Função auxiliar para encontrar a coluna "company"
# ---------------------------------------------------------
def detect_company_column(columns):
    possible_names = [
        "name", "Name", "Company", "company", "Instrument", "Constituent"
    ]
    for col in columns:
        if col in possible_names:
            return col
    return None


# ---------------------------------------------------------
# Scraping da fonte oficial STOXX
# ---------------------------------------------------------
def fetch_from_stoxx():
    try:
        response = requests.get(URL_PRIMARY, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if table is None:
            return None

        df = pd.read_html(str(table))[0]

        # detetar coluna do nome
        company_col = detect_company_column(df.columns)
        if company_col is None:
            return None

        df.rename(columns={company_col: "company"}, inplace=True)

        # normalizar colunas
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        # criar colunas que possam faltar
        for col in ["ticker", "isin", "country", "sector", "subsector", "weight"]:
            if col not in df.columns:
                df[col] = ""

        # manter apenas as colunas necessárias
        return df[["company", "ticker", "isin", "country", "sector", "subsector", "weight"]]

    except Exception:
        return None


# ---------------------------------------------------------
# Scraping do fallback (Investing.com)
# ---------------------------------------------------------
def fetch_from_investing():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_FALLBACK, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        df = pd.read_html(str(table))[0]

        # detetar coluna do nome
        company_col = detect_company_column(df.columns)
        if company_col is None:
            return None

        df.rename(columns={
            company_col: "company",
            "Symbol": "ticker"
        }, inplace=True)

        # criar colunas em falta
        df["isin"] = ""
        df["country"] = ""
        df["sector"] = ""
        df["subsector"] = ""
        df["weight"] = ""

        return df[["company", "ticker", "isin", "country", "sector", "subsector", "weight"]]

    except Exception:
        return None


# ---------------------------------------------------------
# Função principal de scraping
# ---------------------------------------------------------
def fetch_stoxx50_data():
    print("Fetching STOXX 50 data...")

    df = fetch_from_stoxx()
    if df is not None and len(df) >= 40:  # validação mínima
        print("✔ Data loaded from STOXX official website")
        return df

    print("⚠ Official source failed or incomplete, using fallback...")
    df = fetch_from_investing()

    if df is not None and len(df) >= 40:
        print("✔ Data loaded from Investing.com")
        return df

    raise Exception("❌ Failed to fetch STOXX 50 data from all sources.")


# ---------------------------------------------------------
# Guardar ficheiros
# ---------------------------------------------------------
def save_all_formats(df):
    timestamp = datetime.utcnow().isoformat()
    df["last_update"] = timestamp

    df.to_csv("data/stoxx50.csv", index=False)
    df.to_json("data/stoxx50.json", orient="records", indent=4)

    with open("data/stoxx50.md", "w", encoding="utf-8") as f:
        f.write("# STOXX Europe 50 — Constituents\n\n")
        f.write("| Company | Ticker | ISIN | Country | Sector | Subsector | Weight | Last Update |\n")
        f.write("|--------|--------|------|---------|--------|-----------|--------|-------------|\n")
        for _, row in df.iterrows():
            f.write(
                f"| {row['company']} | {row['ticker']} | {row['isin']} | "
                f"{row['country']} | {row['sector']} | {row['subsector']} | "
                f"{row['weight']} | {row['last_update']} |\n"
            )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    df = fetch_stoxx50_data()

    if len(df) != 50:
        print(f"⚠ Warning: Expected 50 companies, got {len(df)}")

    save_all_formats(df)
    print("✔ STOXX 50 dataset updated successfully!")


if __name__ == "__main__":
    main()
