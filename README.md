🔵 **Real-Time Market News Sentiment Monitor** 🔵

---

## 📚 Project Description

This Python application continuously fetches live financial news, analyzes sentiment from each headline, calculates **live market sentiment**, and **logs major changes** — all in **real time**.

✅ Multithreaded  
✅ Lightweight  
✅ Expandable

Designed for everybode who want to monitor **market emotions** from real news headlines.

---

## ✨ Features

- 🚀 **Multithreaded** news fetching and processing
- 🧠 **Sentiment Analysis** of each news item (via TextBlob)
- 📈 **Overall Market Sentiment Tracking** updated live
- 🖍 **Color-coded Console Output** for fast reading
- 🕒 **Cycle Summary** of sentiment change every 60 seconds
- 🛡 **Smart Filtering** — no noisy or empty log entries
- 📂 **CSV Logging** of only meaningful sentiment changes
- 🔔 **Sound Alerts** for strong market news
- 📡 Designed to add **Telegram/Discord alerts** later easily!

---

## 📋 Requirements

- Python 3.8 or higher
- Install required libraries:

```bash
pip install feedparser textblob termcolor
python -m textblob.download_corpora
```

---

## 🛠 How to Run

1. Clone/download this repository

2. Open a terminal (Anaconda Prompt recommended)

3. Navigate to the folder

4. Run the script:

```bash
python newsbot.py
```

---

## 🌐 News Sources Used

- Yahoo Finance

- CNN Money

- MarketWatch

If one feed is empty or down, the bot automatically switches to the next available.

---

## 📂 CSV Output Example
```
Timestamp	Current Sentiment	Sentiment Change
2025-04-13 20:00:00	+0.1540	+0.1540
2025-04-13 20:01:00	+0.1902	+0.0362
2025-04-13 20:02:00	+0.1120	-0.0782
```

✅ Data is only saved if new news was processed during that minute.
✅ Clean and meaningful CSVs

---

## 🖥 Console Output Example

```
[Yahoo Finance] [Neutral +0.00] [Market Sentiment: +0.11] 5 of the Safest Stocks Billionaire Money Managers Bought Ahead of Wall Street's Historic Volatility. 
[Yahoo Finance] [Positive +0.20] [Market Sentiment: +0.11] Like it or not, the bond market rules all. Here's what President Trump's about-face on tariffs this week really means.

📈 Market sentiment improved by +0.11 points. Current Sentiment: +0.11
```

---

## 📈 Future Upgrade Ideas

- Telegram Alerts for strong news

- Live Sentiment Graph plotting

- Stock-Specific Keyword Tracking ("AAPL", "NVDA", "SPY", etc.)

- Integration with Trading APIs (Alpaca, Interactive Brokers)


