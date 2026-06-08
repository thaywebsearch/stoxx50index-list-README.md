#!/usr/bin/env python3
"""
Script para atualizar a tabela do Euro Stoxx 50 a partir da Wikipédia.
Corrige o erro anterior ao processar corretamente o HTML da tabela.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import sys

def fetch_euro_stoxx_50():
    """
    Extrai a tabela do Euro Stoxx 50 da Wikipédia.
    """
    url = "https://en.wikipedia.org/wiki/Euro_Stoxx_50"
    
    try:
        # Headers para simular um browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"[INFO] Página obtida com sucesso. Status: {response.status_code}")
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar todas as tabelas
        tables = soup.find_all('table', {'class': 'wikitable'})
        print(f"[INFO] Encontradas {len(tables)} tabelas na página")
        
        if not tables:
            print("[ERROR] Nenhuma tabela wikitable encontrada")
            return None
        
        # Procurar pela tabela de composição (a que tem Ticker, Name, etc.)
        composition_table = None
        for table in tables:
            headers_row = table.find('tr')
            if headers_row:
                headers_text = headers_row.get_text().lower()
                if 'ticker' in headers_text and 'name' in headers_text:
                    composition_table = table
                    break
        
        if not composition_table:
            # Se não encontrar pela palavra-chave, usar a primeira tabela grande
            print("[INFO] Tabela de composição não encontrada pelo padrão, usando primeira tabela grande")
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) > 40:  # A tabela do Euro Stoxx 50 tem ~50 empresas
                    composition_table = table
                    break
        
        if not composition_table:
            print("[ERROR] Não foi possível identificar a tabela de composição")
            return None
        
        # Extrair dados da tabela
        data = []
        rows = composition_table.find_all('tr')[1:]  # Pular o header
        
        print(f"[INFO] Processando {len(rows)} linhas da tabela")
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:  # Tabela deve ter pelo menos 5 colunas
                continue
            
            try:
                # Extrair dados das colunas
                ticker = cols[0].get_text(strip=True)
                main_listing = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                name = cols[2].get_text(strip=True) if len(cols) > 2 else ""
                corporate_form = cols[3].get_text(strip=True) if len(cols) > 3 else ""
                registered_office = cols[4].get_text(strip=True) if len(cols) > 4 else ""
                sector = cols[5].get_text(strip=True) if len(cols) > 5 else ""
                founded = cols[6].get_text(strip=True) if len(cols) > 6 else ""
                
                # Limpar dados
                ticker = ticker.split('[')[0].strip() if '[' in ticker else ticker
                name = name.split('[')[0].strip() if '[' in name else name
                
                if ticker and name:
                    data.append({
                        'Ticker': ticker,
                        'Main Listing': main_listing,
                        'Name': name,
                        'Corporate Form': corporate_form,
                        'Registered Office': registered_office,
                        'Sector': sector,
                        'Founded': founded
                    })
            except Exception as e:
                print(f"[WARNING] Erro ao processar linha: {e}")
                continue
        
        print(f"[INFO] {len(data)} empresas extraídas com sucesso")
        
        if not data:
            print("[ERROR] Nenhum dado foi extraído da tabela")
            return None
        
        return pd.DataFrame(data)
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Erro ao obter a página: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Erro inesperado: {e}")
        return None

def save_to_csv(df, filename='euro_stoxx_50.csv'):
    """
    Salva o DataFrame em CSV.
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"[INFO] Dados salvos em {filename}")
        print(f"[INFO] Total de registos: {len(df)}")
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao salvar CSV: {e}")
        return False

def main():
    """
    Função principal.
    """
    print(f"[INFO] Iniciando atualização da tabela Euro Stoxx 50 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Obter dados
    df = fetch_euro_stoxx_50()
    
    if df is None or df.empty:
        print("[ERROR] Falha ao obter dados do Euro Stoxx 50")
        sys.exit(1)
    
    # Salvar em CSV
    if not save_to_csv(df):
        sys.exit(1)
    
    # Exibir amostra
    print("\n[INFO] Amostra dos dados:")
    print(df.head(10).to_string())
    
    print(f"\n[INFO] Atualização concluída com sucesso!")
    sys.exit(0)

if __name__ == '__main__':
    main()
