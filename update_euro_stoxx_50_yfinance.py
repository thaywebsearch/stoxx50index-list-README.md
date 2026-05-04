import yfinance as yf
import pandas as pd
import logging
import os
import re
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

FILE_PATH = "euro-stoxx-50-table/euro-stoxx-50-table.md"

def fetch_euro_stoxx_50_data_yfinance():
    # Lista de tickers fornecida pelo utilizador (Euro Stoxx 50)
    tickers = [
        "ADS.DE", "ADYEN.AS", "AD.AS", "AI.PA", "AIR.PA", "ALV.DE", "ABI.BR", "ARGX.BR", "ASML.AS", "CS.PA",
        "BAS.DE", "BAYN.DE", "BBVA.MC", "SAN.MC", "BMW.DE", "BNP.PA", "BN.PA", "DBK.DE", "DB1.DE", "DHL.DE",
        "DTE.DE", "ENEL.MI", "ENI.MI", "EL.PA", "RACE.MI", "RMS.PA", "IBE.MC", "ITX.MC", "IFX.DE", "INGA.AS",
        "ISP.MI", "OR.PA", "MC.PA", "MBG.DE", "MUV2.DE", "NDA-FI.HE", "PRX.AS", "RHM.DE", "SAF.PA", "SGO.PA",
        "SAN.PA", "SAP.DE", "SU.PA", "SIE.DE", "ENR.DE", "TTE.PA", "DG.PA", "UCG.MI", "VOW.DE", "WKL.AS"
    ]
    
    data = []
    for ticker_symbol in tickers:
        try:
            logging.info(f"A obter dados para o ticker: {ticker_symbol}")
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            # Mapeamento de dados para a nossa estrutura
            data.append({
                "Company": info.get("longName", "N/A"),
                "Ticker": ticker_symbol,
                "Country": info.get("country", "N/A"),
                "Sector": info.get("sector", "N/A"),
            })
        except Exception as e:
            logging.error(f"Erro ao obter dados para {ticker_symbol} via yfinance: {e}")
            data.append({
                "Company": "N/A",
                "Ticker": ticker_symbol,
                "Country": "N/A",
                "Sector": "N/A",
            })
            
    df = pd.DataFrame(data)
    logging.info(f"Dados obtidos para {len(df)} empresas via yfinance.")
    return df

def generate_markdown_table(df):
    header = "| Company | Ticker | Country | Sector | Last Update |\n"
    separator = "| :--- | :--- | :--- | :--- | :--- |\n"
    rows = []
    
    current_time = pd.Timestamp.now().isoformat()

    for _, row in df.iterrows():
        company = str(row["Company"]).replace("\n", "").strip()
        ticker = str(row["Ticker"]).replace("\n", "").strip()
        country = str(row["Country"]).replace("\n", "").strip()
        sector = str(row["Sector"]).replace("\n", "").strip()
        
        rows.append(f"| {company} | {ticker} | {country} | {sector} | {current_time} |")
    
    return header + separator + "\n".join(rows) + "\n"

def main():
    logging.info("A iniciar atualização da tabela Euro Stoxx 50 via yfinance...")
    
    try:
        df = fetch_euro_stoxx_50_data_yfinance()
        new_table_content = generate_markdown_table(df)
        
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "# Euro Stoxx 50 — Tabela Completa\n\n"
            os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

        # Regex para encontrar a tabela existente (se houver)
        table_regex = re.compile(r"\| Company \| Ticker \|.*?\n\| :--- \|.*?\n(\|.*?\n)*", re.DOTALL)
        
        if table_regex.search(content):
            logging.info("Tabela existente encontrada. A substituir...")
            updated_content = table_regex.sub(new_table_content, content)
        else:
            logging.info("Tabela não encontrada. A anexar ao final do ficheiro.")
            updated_content = content.rstrip() + "\n\n" + new_table_content
            
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
            
        logging.info("Atualização da tabela Euro Stoxx 50 concluída com sucesso!")

    except Exception as e:
        logging.critical(f"Falha no script de atualização do Euro Stoxx 50: {e}")
        import traceback
        logging.error(traceback.format_exc())
        exit(1)

if __name__ == "__main__":
    main()
