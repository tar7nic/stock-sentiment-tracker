from newsapi import NewsApiClient
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

STOCKS = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'INFY.NS': 'Infosys',
    'HDFCBANK.NS': 'HDFC Bank',
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'GOOGL': 'Google',
    'TSLA': 'Tesla',
    'NVDA': 'Nvidia',
    'AMZN': 'Amazon'
}

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_stock_id(cursor, ticker):
    cursor.execute("SELECT id FROM stocks WHERE ticker = %s", (ticker,))
    result = cursor.fetchone()
    return result[0] if result else None

def fetch_and_store_news():
    conn = get_connection()
    cur = conn.cursor()

    for ticker, company in STOCKS.items():
        print(f"Fetching news for {company}...")
        try:
            response = newsapi.get_everything(
                q=company,
                language='en',
                sort_by='publishedAt',
                page_size=10
            )

            articles = response.get('articles', [])
            print(f"  Found {len(articles)} articles")

            stock_id = get_stock_id(cur, ticker)
            if not stock_id:
                print(f"  {ticker} not in DB, skipping.")
                continue

            for article in articles:
                headline = article.get('title', '')
                source = article.get('source', {}).get('name', '')
                published_at = article.get('publishedAt', None)
                url = article.get('url', '')

                if not headline or headline == '[Removed]':
                    continue

                cur.execute("""
                    INSERT INTO news_sentiment 
                    (stock_id, headline, source, published_at, url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (stock_id, headline, source, published_at, url))

        except Exception as e:
            print(f"  Error fetching {company}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All news fetched and stored!")

if __name__ == "__main__":
    fetch_and_store_news()