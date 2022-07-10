import pandas as pd
import datetime as dt
from util import get_data


def author():
    return "mkurale3"


def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    pricesDF = get_data([symbol], pd.date_range(sd, ed))
    pricesDF = pricesDF.fillna(method="ffill").fillna(method="bfill")
    pricesDF.drop(columns=["SPY"], inplace=True)

    init_pos = (sv, 0, [])  # cash, shares, [transactions]
    positions = [init_pos]

    for i in range(len(pricesDF)):
        price = pricesDF.iloc[i][symbol]
        additional_pos = []
        for pos in positions:
            for trades in [-2000, -1000, 0, 1000, 2000]:
                new_cash_holding = pos[0] - trades * price
                newOrder_transactions = pos[2] + [trades]
                new_shares = pos[1] + trades
                new_pos = (new_cash_holding, new_shares, newOrder_transactions)
                additional_pos.append(new_pos)

        positions = determineBestPositions(additional_pos)

    avgPrice = pricesDF[symbol].mean()
    best_position = max(positions, key=lambda position: position[0] + position[1] * avgPrice)  # determine the best position that maximizes cash holdings
    ordersDF = pd.DataFrame(best_position[2], columns=['Trades'])
    ordersDF['Date'] = pricesDF.index
    ordersDF = ordersDF.set_index('Date')

    return ordersDF


def determineBestPositions(positions):
    best_pos = {}
    for pos in positions:
        cash = pos[0]
        net_holdings = pos[1]
        if net_holdings not in [-1000, 0, 1000]:
            continue
        #update the record if new cash val for existing net holdings is greater
        elif net_holdings in best_pos and cash > best_pos[net_holdings][0]:
            best_pos[net_holdings] = pos
        elif net_holdings not in best_pos:
            best_pos[net_holdings] = pos

    return list(best_pos.values())


def benchMark(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31)):
    pricesDF = get_data(symbol, pd.date_range(sd, ed))
    pricesDF = pricesDF.fillna(method="ffill").fillna(method="bfill")
    pricesDF.drop(columns=["SPY"], inplace=True)

    ordersDF = pd.DataFrame(columns=['Date','Trades'])
    ordersDF['Date'] = pricesDF.index
    ordersDF.loc[0, 'Trades'] = 1000
    ordersDF = ordersDF.set_index('Date')
    ordersDF['Trades'] = ordersDF['Trades'].fillna(0)
    return ordersDF
