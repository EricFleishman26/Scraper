import pandas as pd
import re
import json
from bs4 import BeautifulSoup
import requests


def get_json(ticker, url):
    response = requests.get(url.format(ticker,ticker))
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    script_data = soup.find('script', text=pattern).contents[0]
    start = script_data.find("context")-2
    json_data = json.loads(script_data[start:-12])
    return json_data


def scrape_eps(stock, url):
    json_data = get_json(stock.ticker, url)
    eps = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['trailingEps']['raw']

    return eps

def scrape_growth(stock, url):
    json_data = get_json(stock.ticker, url)
    growth_data = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['earningsTrend']['trend']
    df = pd.DataFrame(growth_data)
    growth = df.loc[4, 'growth']

    return growth['raw']

def scrape_pe(stock, url):
    json_data = get_json(stock.ticker, url)

    try:
        pe = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['trailingPE']['raw']
    except:
        pe = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['forwardPE']['raw']

    return pe

def scrape_fair_value(stock):
    projected_values = get_projected_values(stock)
    return projected_values[0]

def get_projected_values(stock):
    values = []
    projected = []
    earnings = get_earnings(stock)
    pe_ratio = stock.pe_ratio
    divisor = 1 + stock.min_return
    ins_val = earnings[4] * pe_ratio

    for i in range(5):
        if i == 0:
            values.append(ins_val)
        else:
            ins_val = ins_val / divisor
            values.append(ins_val)
    for i in values[::-1]:
        projected.append(i)

    return projected

def get_earnings(stock):
    eps = stock.eps
    growth = stock.growth
    earnings = []

    for i in range(5):
        earnings.append(eps)
        eps = eps + (eps * growth)

    return earnings

def scrape_moving(stock, days, url):
    json_data = get_json(stock.ticker, url)

    if days == 50:
        moving = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['fiftyDayAverage']['raw']
    elif days == 200:
        moving = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['twoHundredDayAverage']['raw']

    return moving
