import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Stock Sentiment Tracker",
    layout="wide"
)

# Title
st.title("Stock Sentiment Tracker")
st.markdown("Real-time stock prices and sentiment analysis for 10 global stocks.")

# Live price ticker
st.subheader("🔴 Live Stock Prices")

TICKERS = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS',
    'AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMZN'
]

@st.cache_data(ttl=75)  # refresh every 5 minutes
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

# Divider
st.divider()

# Looker Studio Dashboard
st.subheader("Sentiment Dashboard")

components.iframe(
    "https://lookerstudio.google.com/embed/reporting/dbaf7419-7ca7-46ef-b2e3-f92a9967f3df/page/RnTpF",
    height=800,
    scrolling=True
)