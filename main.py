import pandas as pd
import sys
import funcs
from classes import *

url_summ = 'https://finance.yahoo.com/quote/{}?p={}'
url_analysis = 'https://finance.yahoo.com/quote/{}/analysis?p={}'
url_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'

tickers = pd.read_csv('data.csv')
df = pd.DataFrame(tickers)

stocks = []

for i in range(len(df)):
    ticker = df.loc[i, "Ticker"].strip()
    stocks.append(Stock(ticker))

while True:
    print("Getting Attributes")
    for i in stocks:
        try:
            print(i.ticker)
            i.eps = funcs.scrape_eps(i, url_summ)
            i.growth = funcs.scrape_growth(i, url_analysis)
            i.pe_ratio = funcs.scrape_pe(i, url_stats)
            i.fair_val = funcs.scrape_fair_value(i)
            i.moving50 = funcs.scrape_moving(i, 50, url_summ)
            i.moving200 = funcs.scrape_moving(i, 200, url_summ)
        except:
            pass

    original_stdout = sys.stdout

    with open('/Users/ericfleishman/Desktop/allinone/scraped_stocks.txt', 'w') as f:
        sys.stdout = f
        print("Ticker EPS Growth P/E Fair Moving50 Moving200")
        for i in stocks:
            print(i.ticker, i.eps, i.growth, i.pe_ratio, i.fair_val, i.moving50, i.moving200)
        sys.stdout = original_stdout


