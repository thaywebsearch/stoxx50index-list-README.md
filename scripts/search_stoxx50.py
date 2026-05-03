import csv
import argparse

def load_data():
    with open("data/stoxx50.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def search(data, key, value):
    return [row for row in data if row[key].lower() == value.lower()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker")
    parser.add_argument("--country")
    parser.add_argument("--sector")
    args = parser.parse_args()

    data = load_data()

    if args.ticker:
        results = search(data, "ticker", args.ticker)
    elif args.country:
        results = search(data, "country", args.country)
    elif args.sector:
        results = search(data, "sector", args.sector)
    else:
        print("No search parameter provided.")
        return

    for r in results:
        print(r)

if __name__ == "__main__":
    main()
