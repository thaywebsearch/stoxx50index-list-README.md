import csv
import argparse
import re

DATA_FILE = "data/stoxx50.csv"

def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def match(value, pattern, regex=False):
    if regex:
        return re.search(pattern, value, re.IGNORECASE) is not None
    return pattern.lower() in value.lower()


def search(data, field, pattern, regex=False):
    return [row for row in data if match(row[field], pattern, regex)]


def print_results(results):
    if not results:
        print("No results found.")
        return

    for r in results:
        print(
            f"{r['company']} ({r['ticker']}) — {r['country']} — "
            f"{r['sector']} — {r['subsector']}"
        )


def main():
    parser = argparse.ArgumentParser(description="Search STOXX 50 dataset")

    parser.add_argument("--ticker", help="Search by ticker")
    parser.add_argument("--company", help="Search by company name")
    parser.add_argument("--country", help="Search by country")
    parser.add_argument("--sector", help="Search by sector")
    parser.add_argument("--subsector", help="Search by subsector")
    parser.add_argument("--regex", action="store_true", help="Enable regex search")

    args = parser.parse_args()
    data = load_data()

    if args.ticker:
        results = search(data, "ticker", args.ticker, args.regex)
    elif args.company:
        results = search(data, "company", args.company, args.regex)
    elif args.country:
        results = search(data, "country", args.country, args.regex)
    elif args.sector:
        results = search(data, "sector", args.sector, args.regex)
    elif args.subsector:
        results = search(data, "subsector", args.subsector, args.regex)
    else:
        print("No search parameter provided.")
        return

    print_results(results)


if __name__ == "__main__":
    main()


