import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

URL_PRIMARY = "https://www.stoxx.com/index-details?symbol=SX5E"
URL_FALLBACK = "https://www.investing.com/indices/stoxx-50-components"

def fetch_from_stoxx():
    """Scrapes the official STOXX website."""
    try:
        response = requests.get(URL_PRIMARY, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if table is None:
            return None

        df = pd.read_html(str(table))[0]

        df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        df.rename(columns={
            "name": "company",
            "isin": "isin",
            "country": "country",
            "industry": "sector"
        }, inplace=True)

        df["subsector"] = ""
        df["weight"] = ""

        return df[["company", "ticker", "isin", "country", "sector", "subsector", "weight"]]

    except Exception:
        return None


def fetch_from_investing():
    """Fallback scraping from Investing.com."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL_FALLBACK, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    df = pd.read_html(str(table))[0]

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


def fetch_stoxx50_data():
    print("Fetching STOXX 50 data...")

    df = fetch_from_stoxx()
    if df is not None:
        print("✔ Data loaded from STOXX official website")
        return df

    print("⚠ Official source failed, using fallback...")
    df = fetch_from_investing()
    print("✔ Data loaded from Investing.com")
    return df


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


