# STOXX 50 Index — Complete Constituents List

A fully maintained, automated and structured dataset containing the complete list of companies included in the **STOXX Europe 50 Index**.

This repository provides:
- Clean and updated datasets (CSV, JSON, Markdown)
- Automated weekly updates via GitHub Actions
- Search utilities for tickers, sectors and countries
- A minimalistic and professional structure for long‑term maintenance

---

## 📊 Dataset Contents

Each entry includes:
- Company Name  
- Ticker  
- ISIN  
- Country  
- Sector  
- Subsector  
- Weight (if available)  
- Last Update Timestamp  

---

## 📁 Repository Structure

```
data/       → CSV, JSON and Markdown versions of the index  
scripts/    → Automation and search utilities  
.github/    → GitHub Actions workflow for weekly updates  
README.md   → Documentation  
```

---

## 🤖 Automation

The dataset is automatically updated every week using:

- `scripts/update_stoxx50.py`
- GitHub Actions workflow (`update.yml`)

If new companies enter or leave the index, the dataset updates automatically.

---

## 🔍 Search Tools

Use:

```
python scripts/search_stoxx50.py --ticker <TICKER>
python scripts/search_stoxx50.py --country <COUNTRY>
python scripts/search_stoxx50.py --sector <SECTOR>
```

---

## 📄 Data Sources

The STOXX Europe 50 constituents are based on publicly available composition files and financial data providers.

---

## 📜 License

MIT License.

