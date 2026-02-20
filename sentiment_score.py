from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

analyzer = SentimentIntensityAnalyzer()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_sentiment_label(compound):
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def score_all_headlines():
    conn = get_connection()
    cur = conn.cursor()

    # Fetch all unscored headlines
    cur.execute("""
        SELECT id, headline FROM news_sentiment
        WHERE vader_compound IS NULL
    """)
    rows = cur.fetchall()
    print(f"Found {len(rows)} unscored headlines...")

    for row_id, headline in rows:
        scores = analyzer.polarity_scores(headline)

        compound = scores['compound']
        label = get_sentiment_label(compound)

        cur.execute("""
            UPDATE news_sentiment
            SET vader_positive = %s,
                vader_negative = %s,
                vader_neutral = %s,
                vader_compound = %s,
                sentiment_label = %s
            WHERE id = %s
        """, (
            scores['pos'],
            scores['neg'],
            scores['neu'],
            compound,
            label,
            row_id
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All headlines scored!")

if __name__ == "__main__":
    score_all_headlines()