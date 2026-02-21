# 📈 Stock Sentiment Tracker

A real-time stock sentiment analysis pipeline that monitors 10 global stocks by combining live price data with news sentiment scoring, visualized through an interactive dashboard.

## 🔗 Live Demo
[View Streamlit App](https://stock-sentiment-tracker-tn019.streamlit.app/)

## 📌 Overview
This project tracks 10 Indian and US stocks, pulls financial news headlines, scores them using VADER sentiment analysis, and visualizes the relationship between news sentiment and stock price movements.

## 🛠️ Tech Stack
- **Python** — Data pipeline and scripting
- **yfinance** — Live and historical stock price data
- **NewsAPI** — Financial news headlines
- **VADER** — NLP sentiment scoring
- **PostgreSQL (Supabase)** — Cloud database
- **Looker Studio** — Interactive dashboard
- **Streamlit** — Web application
- **GitHub Actions** — Automated pipeline every 6 hours

## ⚙️ Architecture
```
NewsAPI + yfinance → Python Scripts → Supabase (PostgreSQL) → Looker Studio + Streamlit
```

## 📁 Project Structure
```
stock-sentiment-tracker/
├── fetch_prices.py        # Fetches stock prices from yfinance
├── fetch_news.py          # Fetches news headlines from NewsAPI
├── sentiment_score.py     # Scores headlines using VADER
├── app.py                 # Streamlit web application
├── requirements.txt       # Python dependencies
├── .github/
│   └── workflows/
│       └── pipeline.yml   # GitHub Actions automation
└── .gitignore
```

## 📈 Dashboard Features
- **Stock Price Trends** — 30-day closing price for all 10 stocks
- **Sentiment vs Price Movement** — Scatter plot correlating news sentiment with price change %
- **Sentiment Rankings** — Bar chart ranking stocks by average sentiment score