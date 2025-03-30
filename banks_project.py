import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
import logging

EXCHANGE_RATE_CSV_PATH = './exchange_rate.csv'
EXTRACTION_TABLE_ATTRIBUTES = ['Name','MC_USD_Billion']
FINAL_TABLE_ATTRIBUTES = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']

OUTPUT_CSV_PATH = './Largest_banks_data.csv'
DB_NAME = 'Banks.db'
TABLE_NAME = 'Largest_banks'
LOG_FILE = './code_log.txt'

DATA_URL = 'https://en.wikipedia.org/wiki/List_of_largest_banks'

# Set up logging configuration
logging.basicConfig(
    filename=LOG_FILE,  # Log file
    level=logging.DEBUG,  # Capture all log levels
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
    encoding='utf-8'
)

def log_progress(status_msg:str,level):
    if level == 'INFO':
        logging.info(status_msg)
    if level == 'ERROR':
        logging.error(status_msg,exc_info=True)

def extract(url:str,attributes:list[str]):
    try:
        log_progress(f"Data Extraction Started...",level='INFO')
        dfe = pd.DataFrame(columns=attributes)

        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        table = soup.find('table')
        body = table.find('tbody')

        row_list = body.find_all('tr')
        row_list.remove(row_list[0]) # remove heading row

        for i,row in enumerate(row_list):
            if i > 9 :
                break

            cols = row.find_all('td')

            bank_name = cols[1].find_all('a')[1].get_text(strip=True)
            mc_usd_billion = cols[2].get_text(strip=True)

            df1 = pd.DataFrame(data={
                'Name' : bank_name.strip(),
                'MC_USD_Billion' : float(mc_usd_billion.replace(',','').strip())
            },index=[0])

            dfe = pd.concat([dfe,df1],ignore_index=True)

        log_progress(f"Data Extraction Completed...\n{dfe}\n",level='INFO')

        return dfe

    except Exception as ee:
        log_progress(f"Failed To Extract Data : {ee}",level='ERROR')

def transform(bank_data:pd.DataFrame,exchange_rate_csv:str):
    try:
        log_progress("Data Transform Started...",level="INFO")

        exchange_rates = pd.read_csv(exchange_rate_csv)
        exchange_rates_dict = exchange_rates.set_index("Currency")["Rate"].to_dict()

        dft = pd.DataFrame(columns=FINAL_TABLE_ATTRIBUTES)
        dft["Name"] = bank_data["Name"]
        dft["MC_USD_Billion"] = bank_data["MC_USD_Billion"]
        dft['MC_GBP_Billion'] = bank_data["MC_USD_Billion"] * exchange_rates_dict["GBP"]
        dft['MC_EUR_Billion'] = bank_data["MC_USD_Billion"] * exchange_rates_dict["EUR"]
        dft['MC_INR_Billion'] = bank_data["MC_USD_Billion"] * exchange_rates_dict["INR"]

        log_progress(f"Data Transform Completed...\n{dft}\n",level="INFO")

        return dft.round(2)

    except Exception as et:
        log_progress(f"Failed To Transform Data : {et}",level="ERROR")

def load_to_csv(data_frame:pd.DataFrame,csv_path:str):
    try:
        log_progress(f"Loading Data Into Csv File...",level="INFO")
        data_frame.to_csv(csv_path)
        log_progress(f"Data Loaded Successfully In Csv",level="INFO")
    except Exception as ec:
        log_progress(f"Data Loading Into Csv Failed : {ec}",level="ERROR")

def load_to_db(data_frame:pd.DataFrame,database_file_name:str,table_name:str):
    try:
        log_progress(f"Loading Data Into DataBase...",level="INFO")
        conn = sqlite3.connect(database_file_name)
        data_frame.to_sql(table_name,conn,if_exists='replace',index=False)
        conn.close()
        log_progress(f"Data Loaded Successfully Into Database",level="INFO")
    except Exception as ed:
        log_progress(f"Data Loading Into Database Failed : {ed}",level="ERROR")

def execute_query(cur,query):
    cur.execute(query)
    rows = cur.fetchall()
    log_progress(f"query {query} successfully executed : {rows}", level="INFO")

    print(f"query {query}")
    print(f"results : ")

    for row in rows:
        print(row)
    print()


def run_queries(db_file:str,table_name:str):
    try:
        log_progress(f"Initiating connection with db-{db_file}...",level="INFO")
        conn = sqlite3.connect(db_file)
        log_progress(f"Connection Successful with db-{db_file}",level='INFO')
        cursor = conn.cursor()

        query1 = f'SELECT * FROM {table_name};'
        query2 = f'SELECT AVG(MC_GBP_Billion) FROM {table_name};'
        query3 = f'SELECT Name from {table_name} LIMIT 5;'

        execute_query(cursor, query1)
        execute_query(cursor, query2)
        execute_query(cursor, query3)

        conn.close()

        log_progress(f"Connection Closed",level="INFO")
        log_progress(f"Queries Executed Successfully",level="INFO")

    except Exception as er:
        log_progress(f"Queries Failed on Database {db_file} : {er}",level="ERROR")

log_progress("ETL Pipeline Started",level='INFO')

try:
    df = extract(DATA_URL,attributes=EXTRACTION_TABLE_ATTRIBUTES)
    final_df = transform(df,EXCHANGE_RATE_CSV_PATH)
    load_to_csv(final_df,OUTPUT_CSV_PATH)
    load_to_db(final_df,DB_NAME,TABLE_NAME)
    run_queries(DB_NAME,TABLE_NAME)
except Exception as e:
    log_progress(f'Exception : {e}',level='ERROR')

log_progress("ETL Pipeline Completed",level='INFO')