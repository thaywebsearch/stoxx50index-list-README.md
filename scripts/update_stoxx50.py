import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO

URL_PRIMARY = "https://www.stoxx.com/index-details?symbol=SX5E"
URL_FALLBACK = "https://www.investing.com/indices/stoxx-50-components"
URL_WIKIPEDIA = "https://en.wikipedia.org/wiki/EURO_STOXX_50"


def fetch_from_stoxx():
    """Scrapes the official STOXX website."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_PRIMARY, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if table is None:
            return None

        df = pd.read_html(StringIO(str(table)))[0]
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        df.rename(columns={
            "name": "company",
            "isin": "isin",
            "country": "country",
            "industry": "sector"
        }, inplace=True)

        df["subsector"] = ""
        df["weight"] = ""

        if "ticker" not in df.columns:
            df["ticker"] = ""

        return df[["company", "ticker", "isin", "country", "sector", "subsector", "weight"]]

    except Exception:
        return None


def fetch_from_investing():
    """Fallback scraping from Investing.com."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_FALLBACK, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if table is None:
            return None

        df = pd.read_html(StringIO(str(table)))[0]

        df.rename(columns={
            "Name": "company",
            "Symbol": "ticker"
        }, inplace=True)

        df["isin"] = ""
        df["country"] = ""
        df["sector"] = ""
        df["subsector"] = ""
        df["weight"] = ""

        return df[["company", "ticker", "isin", "country", "sector", "subsector", "weight"]]

    except Exception:
        return None


def fetch_from_wikipedia():
    """Fallback final: scraping da Wikipedia (sempre disponível)."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_WIKIPEDIA, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # A Wikipedia tem várias tabelas, procuramos a que tem "Ticker"
        tables = soup.find_all("table", {"class": "wikitable"})
        for table in tables:
            df = pd.read_html(StringIO(str(table)))[0]
            if "Ticker" in df.columns or "ticker" in df.columns:
                df.columns = [c.strip() for c in df.columns]
                df.rename(columns={
                    "Company": "company",
                    "Ticker": "ticker",
                    "ISIN": "isin",
                    "Country": "country",
                    "Sector": "sector",
                    "Sub-sector": "subsector"
                }, inplace=True)

                for col in ["company", "ticker", "isin", "country", "sector", "subsector"]:
                    if col not in df.columns:
                        df[col] = ""

                df["weight"] = ""
                return df[["company", "ticker", "isin", "country", "sector", "subsector", "weight"]]

        return None

    except Exception:
        return None


def fetch_stoxx50_data():
    print("Fetching STOXX 50 data...")

    df = fetch_from_stoxx()
    if df is not None:
        print("✔ Data loaded from STOXX official website")
        return df

    print("⚠ Official source failed, trying Investing.com...")
    df = fetch_from_investing()
    if df is not None:
        print("✔ Data loaded from Investing.com")
        return df

    print("⚠ Investing.com failed, trying Wikipedia...")
    df = fetch_from_wikipedia()
    if df is not None:
        print("✔ Data loaded from Wikipedia")
        return df

    raise RuntimeError("❌ All sources failed. Could not fetch STOXX 50 data.")


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


def main():
    df = fetch_stoxx50_data()
    save_all_formats(df)
    print("✔ STOXX 50 dataset updated successfully!")


if __name__ == "__main__":
    main()
