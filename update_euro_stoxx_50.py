import requests
import pandas as pd
from bs4 import BeautifulSoup
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

def fetch_euro_stoxx_50_data(retries=3, backoff=2):
    url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
    
    # User-Agent altamente específico conforme a política da Wikipédia
    # Inclui o nome do script e um contacto genérico (pode ser o link do repo)
    request_headers = { # Renomeado para evitar conflito
        'User-Agent': 'EuroStoxx50Bot/1.0 (https://github.com/thaywebsearch/euro-stoxx-50-list; mailto:admin@example.com) python-requests/2.31.0',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    for attempt in range(retries):
        try:
            logging.info(f"Tentativa {attempt + 1}: Acedendo à Wikipédia para Euro Stoxx 50...")
            response = requests.get(url, headers=request_headers, timeout=20) # Usar request_headers
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # A tabela de constituintes não tem um ID específico, mas está sob um cabeçalho "Composition"
            # Vamos procurar pelo cabeçalho e depois pela tabela seguinte
            composition_heading = soup.find("span", {"id": "Composition"})
            if not composition_heading:
                composition_heading = soup.find("span", string="Composition") # Fallback para texto

            table = None
            if composition_heading:
                # Encontrar a próxima tabela após o cabeçalho de composição
                current_element = composition_heading.find_parent().find_next_sibling()
                while current_element:
                    if current_element.name == "table":
                        table = current_element
                        break
                    current_element = current_element.find_next_sibling()
            
            if not table:
                # Fallback: procurar por qualquer tabela que contenha 'Ticker' e 'Name'
                tables = soup.find_all("table", class_="wikitable") # Muitas tabelas são 'wikitable'
                for t in tables:
                    table_headers = [th.get_text(strip=True) for th in t.find_all("th")] # Renomeado para evitar conflito
                    if "Ticker" in table_headers and "Name" in table_headers:
                        table = t
                        break

            if not table:
                raise ValueError("Não foi possível localizar a tabela de constituintes do Euro Stoxx 50 na página.")

            df = pd.read_html(str(table))[0]
            df.columns = [str(c).strip() for c in df.columns]
            
            logging.info(f"Sucesso! {len(df)} empresas encontradas para Euro Stoxx 50.")
            return df

        except Exception as e:
            logging.error(f"Erro na tentativa {attempt + 1} de obter dados do Euro Stoxx 50: {e}")
            if attempt < retries - 1:
                time.sleep(backoff * (attempt + 1))
            else:
                raise

def generate_markdown_table(df):
    # Mapear nomes de colunas esperados para os nomes reais no DataFrame
    col_map = {
        'Ticker': next((c for c in df.columns if 'Ticker' in c), None),
        'Name': next((c for c in df.columns if 'Name' in c), None),
        'Country': next((c for c in df.columns if 'Registered office' in c or 'Country' in c), None),
        'Sector': next((c for c in df.columns if 'Sector' in c), None),
    }
    
    if not all(col_map.values()):
        logging.error(f"Colunas detetadas: {df.columns.tolist()}")
        raise KeyError(f"Não foi possível mapear todas as colunas necessárias. Mapeamento: {col_map}")

    header = "| Company | Ticker | Country | Sector | Last Update |\n"
    separator = "| :--- | :--- | :--- | :--- | :--- |\n"
    rows = []
    
    current_time = pd.Timestamp.now().isoformat()

    for _, row in df.iterrows():
        company = str(row[col_map['Name']]).replace('\n', '').strip()
        ticker = str(row[col_map['Ticker']]).replace('\n', '').strip()
        country = str(row[col_map['Country']]).replace('\n', '').strip()
        sector = str(row[col_map['Sector']]).replace('\n', '').strip()
        
        rows.append(f"| {company} | {ticker} | {country} | {sector} | {current_time} |")
    
    return header + separator + "\n".join(rows) + "\n"

def main():
    logging.info("A iniciar atualização da tabela Euro Stoxx 50...")
    
    try:
        df = fetch_euro_stoxx_50_data()
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

