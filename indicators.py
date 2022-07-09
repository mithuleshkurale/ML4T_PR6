import matplotlib.pyplot as plt
import pandas as pd
from util import get_data

def author():
    return 'mkurale3'

def getBollingerBands(pricesDF):
    rm_JPM = pricesDF["JPM"].rolling(30).mean()
    rstd_JPM = pricesDF["JPM"].rolling(30).std()
    upper_bound = rm_JPM + rstd_JPM * 2
    lower_bound = rm_JPM - rstd_JPM * 2

    ax = pricesDF['JPM'].plot(title="Bollinger Bands", label='JPM')
    rm_JPM.plot(labels='Rolling mean', ax=ax)
    upper_bound.plot(labels='Upper bound', ax=ax)
    lower_bound.plot(labels='Lower bound', ax=ax)
    plt.savefig('Figure2.png')
    plt.clf()
    # pricesDF["SMA"] = rm_JPM
    # pricesDF["Upper Bol"] = upper_bound
    # pricesDF["Lower Bol"] = lower_bound

def getSimpleMovingAverage(pricesDF):
    rm_JPM = pricesDF["JPM"].rolling(30).mean()
    price_sma = pricesDF["JPM"]/rm_JPM

    ax = pricesDF['JPM'].plot(title="SMA & Price/SMA", label='JPM')
    rm_JPM.plot(labels='Rolling mean', ax=ax)
    price_sma.plot(labels='Price/SMA', ax=ax)
    plt.savefig('Figure3.png')
    plt.clf()

def getMomentum(pricesDF):
    momentum = pricesDF['JPM']/pricesDF['JPM'].shift(30)-1
    ax = pricesDF['JPM'].plot(title="Momentum", label='JPM')
    momentum.plot(labels='Momentum', ax=ax)
    plt.savefig('Figure4.png')
    plt.clf()

def getMACD(pricesDF):
    twelve_day_EMA = pricesDF['JPM'].ewm(span=12).mean()
    twenty_six_day_EMA = pricesDF['JPM'].ewm(span=26).mean()
    MACD = twelve_day_EMA - twenty_six_day_EMA
    macd_trigger = MACD.ewm(soan=9).mean()
    divergence_convergence = maced - macd_trigger
    ax = pricesDF['JPM'].plot(title="MACD", label='JPM')
    MACD.plot(labels='MACD', ax = ax)
    macd_trigger.plot(labels='Signal', ax=ax)
    divergence_convergence.plot(labels='CrossOver', ax=ax)
    plt.savefig('Figure5.png')
    plt.clf

def getPercentagePriceCalculator(pricesDF):
    twelve_day_EMA = pricesDF['JPM'].ewm(span=12).mean()
    twenty_six_day_EMA = pricesDF['JPM'].ewm(span=26).mean()
    MACD = twelve_day_EMA - twenty_six_day_EMA
    PPO = (MACD/twenty_six_day_EMA) * 100

    ax = pricesDF['JPM'].plot(title="Price Percentage Indicator", label='JPM')
    PPO.plot(labels='PPO',ax =ax)
    plt.savefig('Figure6.png')
    plt.clf()

def run():
    pricesDF = get_data(["JPM"], pd.date_range("2008-01-01", "2009-12-31"))
    pricesDF = pricesDF.fillna(method="ffill").fillna(method="bfill")
    pricesDF.drop(columns=["SPY"], inplace=True)
    pricesDF_norm = pricesDF / pricesDF.iloc[0]

    getBollingerBands(pricesDF_norm)
    getSimpleMovingAverage(pricesDF_norm)
    getMomentum(pricesDF_norm)
    getMACD(pricesDF)
