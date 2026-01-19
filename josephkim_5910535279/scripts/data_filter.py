import os
import csv
from bs4 import BeautifulSoup


input_file = "../data/raw_data/web_data.html"

market_csv = "../data/processed_data/market_data.csv"
news_csv = "../data/processed_data/news_data.csv"

print("Reading web_data.html")
with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

#print("HTML length:", len(html))
#print("Contains MarketCard-container?:", "MarketCard-container" in html)

# use bs4's built in html parser to separate html file by sections (?), classes
soup = BeautifulSoup(html, "html.parser")
#print("Total <a> tags:", len(soup.find_all("a")))

print("Filtering market banner fields")

market_rows = []
cards = soup.find_all(class_=lambda c: c and "MarketCard-container"in c)
#print(cards)

for card in cards: 
    symbol = card.find("span", class_="MarketCard-symbol")
    pos = card.find("span", class_="MarketCard-stockPosition")
    pct = card.find("span", class_="MarketCard-changesPct")

    if not (symbol and pos and pct):
        continue

    market_rows.append({
        "MarketCard_symbol": symbol.get_text(strip=True),
        "MarketCard_stockPosition": pos.get_text(strip=True),
        "MarketCard_changePct": pct.get_text(strip=True),
        })

#print(market_rows)
with open(market_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
            f, 
            fieldnames=[
                "MarketCard_symbol",
                "MarketCard_stockPosition",
                "MarketCard_changePct"
                ]
            )
    writer.writeheader()
    writer.writerows(market_rows)

print("Market data written to:", market_csv)

# much of the same code except now with the 'li' 'LatestNews' items instead of Market
print("Extracting Latest News data:")

news_rows = []

items = soup.find_all("li", class_="LatestNews-item")
print(len(items))

for item in items:
    time_tag = item.find("time", class_="LatestNews-timestamp")
    title_tag = item.find("a", class_="LatestNews-headline")

    if not (time_tag and title_tag):
        continue

    news_rows.append({
        "Timestamp": time_tag.get_text(strip=True),   
        "Title": title_tag.get_text(strip=True),
        "Link": title_tag.get("href")
        })

print("News extraction success")

with open(news_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
            f,
            fieldnames=["Timestamp", "Title", "Link"]
            )
    writer.writeheader()
    writer.writerows(news_rows)

print("News data written to:", news_csv)

