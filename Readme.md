# ETL Pipeline: Largest Banks Data Scraper

![ETL Pipeline](https://img.shields.io/badge/ETL-Pipeline-blue.svg) ![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg) ![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg) ![Web Scraping](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup-lightblue.svg)

## 📌 Project Overview
This project is an **ETL (Extract, Transform, Load) pipeline** that scrapes market capitalization data of the world's largest banks from Wikipedia, converts the values into different currencies, and stores the results in both CSV format and an SQLite database.

## ✨ Features
- **Web Scraping**: Extracts bank data using `requests` and `BeautifulSoup`
- **Data Transformation**: Converts market capitalization (USD) to GBP, EUR, and INR using exchange rates
- **Database Storage**: Saves the transformed data into an SQLite database
- **Logging**: Implements error handling and logs progress for debugging
- **CSV Export**: Saves the final processed data into a CSV file

## 🛠 Technologies Used
- **Python** 🐍
- `requests` – Fetches the Wikipedia page
- `BeautifulSoup` – Parses and extracts tabular data
- `pandas` – Processes and transforms data
- `sqlite3` – Stores structured data in a relational database
- `logging` – Captures execution logs for debugging

## 📂 Project Structure
```plaintext
📁 Etl-PipeLine-Banks/
│-- main.py                 # Main script for the ETL process
│-- exchange_rate.csv       # Exchange rates for currency conversion
│-- Banks.db                # SQLite database (generated after execution)
│-- Largest_banks_data.csv  # Final processed data (generated after execution)
│-- code_log.txt            # Execution log file
│-- README.md               # Project documentation
```

## 🔧 Installation & Usage
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/codetitan69/Etl-PipeLine-Banks.git
cd Etl-PipeLine-Banks
```
### 2️⃣ Install Dependencies
Ensure you have Python 3.8+ installed, then install the required libraries:
```bash
pip install requests pandas beautifulsoup4 sqlite3
```
### 3️⃣ Run the ETL Pipeline
```bash
python main.py
```
### 4️⃣ View the Results
- Processed data is saved in `Largest_banks_data.csv`
- Database file `Banks.db` contains structured data for queries
- Execution logs can be checked in `code_log.txt`

## 📊 SQL Queries
To run queries on the database, you can use:
```sql
SELECT * FROM Largest_banks;
SELECT AVG(MC_GBP_Billion) FROM Largest_banks;
SELECT Name FROM Largest_banks LIMIT 5;
```

## 📝 Future Improvements
- Add support for more currencies
- Automate exchange rate fetching from an API
- Implement error handling for dynamic Wikipedia table changes

## 🤝 Contributing
Feel free to fork this repository, raise issues, or suggest improvements! 🚀

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---
📌 **Author**: [codetitan69](https://github.com/codetitan69)  
📌 **GitHub Repository**: [Etl-PipeLine-Banks](https://github.com/codetitan69/Etl-PipeLine-Banks)  
📌 **Feel free to ⭐ the repo if you found it useful!**
