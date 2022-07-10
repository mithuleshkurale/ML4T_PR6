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
    percent_B = (pricesDF["JPM"] - lower_bound / pricesDF["JPM"] - upper_bound) * 100

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, squeeze=True,
             subplot_kw=None, gridspec_kw=None)

    pricesDF['JPM'].plot(ax=ax1)
    rm_JPM.plot(ax=ax1)
    upper_bound.plot(ax=ax1)
    lower_bound.plot(ax=ax1)
    ax1.set_title("Bollinger Bands and %B Indicator 30 Days")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax1.legend(['Price', 'Rolling mean', "Upper Bound", "Lower Bound"])
    percent_B.plot(ax=ax2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("%B")
    plt.savefig('Figure2.png')
    plt.close()


def getSimpleMovingAverage(pricesDF):
    rm_JPM = pricesDF["JPM"].rolling(30).mean()
    price_sma = pricesDF["JPM"] / rm_JPM

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, squeeze=True,
                                   subplot_kw=None, gridspec_kw=None)

    pricesDF['JPM'].plot(ax=ax1)
    rm_JPM.plot(ax=ax1)
    price_sma.plot(ax=ax2)
    ax1.set_title("SMA 30 days")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax1.legend(['JPM Price', 'Rolling mean'])
    ax2.set_ylabel('Price/SMA')
    plt.savefig('Figure3.png')
    plt.close()


def getMomentum(pricesDF):
    momentum = pricesDF['JPM'] / pricesDF['JPM'].shift(30) - 1
    ax = pricesDF['JPM'].plot()
    momentum.plot(ax=ax)
    plt.title("Momentum 30 days")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(["JPM Price", "Momentum"])
    plt.savefig('Figure4.png')
    plt.close()


def getMACD(pricesDF):
    twelve_day_EMA = pricesDF['JPM'].ewm(span=12).mean()
    twenty_six_day_EMA = pricesDF['JPM'].ewm(span=26).mean()
    MACD = twelve_day_EMA - twenty_six_day_EMA
    signal = MACD.ewm(span=9).mean()
    histogram = MACD - signal
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, squeeze=True,
                                   subplot_kw=None, gridspec_kw=None)
    pricesDF['JPM'].plot(ax=ax1)
    MACD.plot(ax=ax2)
    signal.plot(ax=ax2)
    histogram.plot(ax=ax2)
    ax1.set_title("MACD Indicator")
    ax2.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax2.set_ylabel("MACD")
    ax2.legend(['MACD', "signal", "histogram"])
    plt.savefig('Figure5.png')
    plt.close()


def getPercentagePriceCalculator(pricesDF):
    twelve_day_EMA = pricesDF['JPM'].ewm(span=12).mean()
    twenty_six_day_EMA = pricesDF['JPM'].ewm(span=26).mean()
    MACD = twelve_day_EMA - twenty_six_day_EMA
    PPO = (MACD / twenty_six_day_EMA) * 100

    # ax = pricesDF['JPM'].plot(title="Price Percentage Indicator", label='JPM')
    PPO.plot()
    plt.title("Price Percentage Indicator")
    plt.xlabel("Date")
    plt.ylabel("% Price")
    plt.legend(['% Price'])
    plt.savefig('Figure6.png')
    plt.close()


def run():
    pricesDF = get_data(["JPM"], pd.date_range("2008-01-01", "2009-12-31"))
    pricesDF = pricesDF.fillna(method="ffill").fillna(method="bfill")
    pricesDF.drop(columns=["SPY"], inplace=True)
    pricesDF_norm = pricesDF / pricesDF.iloc[0]

    getBollingerBands(pricesDF_norm)
    getSimpleMovingAverage(pricesDF_norm)
    getMomentum(pricesDF_norm)
    getMACD(pricesDF_norm)
    getPercentagePriceCalculator(pricesDF_norm)
