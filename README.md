# STOXX Europe 50 Index — Complete Constituents Dataset

A clean, structured and automatically updated dataset containing all companies included in the **STOXX Europe 50 Index (SX5E)**.  
Updated weekly via GitHub Actions and available in **CSV**, **JSON** and **Markdown** formats.

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
data/
  ├── stoxx50.csv
  ├── stoxx50.json
  └── stoxx50.md

scripts/
  ├── update_stoxx50.py
  └── search_stoxx50.py

.github/
  └── workflows/
      └── update.yml

README.md
```

---

## 🤖 Automation

This repository updates automatically every week using:

- `scripts/update_stoxx50.py` (scraping + data processing)
- GitHub Actions workflow (`update.yml`)

If the index composition changes, the dataset is refreshed and committed automatically.

---

## 🔍 Search Tool

Search the dataset locally:

```
python scripts/search_stoxx50.py --ticker ASML
python scripts/search_stoxx50.py --company nestle
python scripts/search_stoxx50.py --country France
python scripts/search_stoxx50.py --sector Technology
python scripts/search_stoxx50.py --regex --company "^(A|B)"
```

Supports:

- partial match  
- case‑insensitive search  
- regex mode  

---

## 🌐 Data Sources

The STOXX Europe 50 constituents are based on publicly available index composition data from:

- STOXX official website  
- Investing.com (fallback source)

---

## 📄 Formats

### **CSV**
`data/stoxx50.csv`

### **JSON**
`data/stoxx50.json`

### **Markdown**
`data/stoxx50.md`

---

## 🏷️ Badges

![Auto Update](https://img.shields.io/badge/Update-Automated-success)
![Data Format](https://img.shields.io/badge/Formats-CSV%20%7C%20JSON%20%7C%20MD-blue)
![Index](https://img.shields.io/badge/Index-STOXX%2050-orange)

---

## 📜 License

MIT License.

---

## ⭐ Contribute

Pull requests and suggestions are welcome.
