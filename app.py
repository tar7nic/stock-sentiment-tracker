import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Stock Sentiment Tracker",
    layout="wide"
)

# Title
st.title("Stock Sentiment Tracker")
st.markdown("""
This app monitors **10 global stocks** (Indian & US) in real time by combining 
live price data with news sentiment analysis. Prices refresh every 60 seconds 
and the sentiment dashboard updates every 12 hours automatically.
""")

st.divider()

# Live price ticker
st.subheader("🔴 Live Stock Prices")

TICKERS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS',
    'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMZN'
]

@st.cache_data(ttl=60)  
def get_live_prices():
    data = []
    for ticker in TICKERS:
        stock = yf.Ticker(ticker)
        info = stock.fast_info
        data.append({
            'Ticker': ticker,
            'Current Price': round(info.last_price, 2),
            'Previous Close': round(info.previous_close, 2),
            'Change %': round(((info.last_price - info.previous_close) / info.previous_close) * 100, 2)
        })
    return pd.DataFrame(data)

df = get_live_prices()

# Color the Change % column
def color_change(val):
    color = 'green' if val > 0 else 'red'
    return f'color: {color}'

df.index = range(1,len(df) + 1)
st.dataframe(
    df.style.applymap(color_change, subset=['Change %']),
    use_container_width=True
)

st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

# Divider
st.divider()

# Looker Studio Dashboard
st.subheader("Sentiment Dashboard")

components.iframe(
    "https://lookerstudio.google.com/embed/reporting/dbaf7419-7ca7-46ef-b2e3-f92a9967f3df/page/RnTpF",
    height=800,
    scrolling=True
)
