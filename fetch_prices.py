import yfinance as yf
import psycopg2
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

TICKERS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS',
    'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMZN'
]

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_stock_id(cursor, ticker):
    cursor.execute("SELECT id FROM stocks WHERE ticker = %s", (ticker,))
    result = cursor.fetchone()
    return result[0] if result else None

def fetch_and_store_prices():
    conn = get_connection()
    cur = conn.cursor()

    for ticker in TICKERS:
        print(f"Fetching {ticker}...")
        stock = yf.Ticker(ticker)
        hist = stock.history(period="30d")  # last 30 days of data

        if hist.empty:
            print(f"  No data for {ticker}, skipping.")
            continue

        stock_id = get_stock_id(cur, ticker)
        if not stock_id:
            print(f"  {ticker} not found in stocks table, skipping.")
            continue

        for record_date, row in hist.iterrows():
            # Calculate % change
            open_p = round(float(row['Open']), 4)
            close_p = round(float(row['Close']), 4)
            change_pct = round(((close_p - open_p) / open_p) * 100, 4)

            cur.execute("""
                INSERT INTO prices (stock_id, date, open_price, high_price, low_price, close_price, volume, price_change_pct)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (stock_id, date) DO NOTHING
            """, (
                stock_id,
                record_date.date(),
                open_p,
                round(float(row['High']), 4),
                round(float(row['Low']), 4),
                close_p,
                int(row['Volume']),
                change_pct
            ))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All prices fetched and stored!")

if __name__ == "__main__":
    fetch_and_store_prices()