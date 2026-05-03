import csv
import json
from datetime import datetime

def fetch_stoxx50_data():
    # TODO: Add scraping or API logic
    return []

def save_csv(data):
    with open("data/stoxx50.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["company","ticker","isin","country","sector","subsector","weight","last_update"])
        writer.writerows(data)

def save_json(data):
    with open("data/stoxx50.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def save_markdown(data):
    with open("data/stoxx50.md", "w", encoding="utf-8") as f:
        f.write("# STOXX 50 Index — Constituents\n\n")
        f.write("| Company | Ticker | ISIN | Country | Sector | Subsector | Weight | Last Update |\n")
        f.write("|--------|--------|------|---------|--------|-----------|--------|-------------|\n")
        for row in data:
            f.write("| " + " | ".join(row) + " |\n")

def main():
    data = fetch_stoxx50_data()
    timestamp = datetime.utcnow().isoformat()

    # Add timestamp to each row
    data = [row + [timestamp] for row in data]

    save_csv(data)
    save_json(data)
    save_markdown(data)

if __name__ == "__main__":
    main()
