import pandas as pd
from util import get_data
from collections import namedtuple

Position = namedtuple("Pos", ["cash", "shares", "transactions"])


def author():
    return "felixm"


def new_positions(positions, price):
    """Calculate all potential new positions and then keep the best three."""
    # Execute all possible transactions
    new_positions = []
    for p in positions:
        for t in [-2000, -1000, 0, 1000, 2000]:
            ts = p.transactions + [t]
            p_new = Position(p.cash - t * price, p.shares + t, ts)
            new_positions.append(p_new)

    # Keep the positions with the highest cash value for each amount of shares.
    best = {}
    for p in new_positions:
        if p.shares not in [-1000, 0, 1000]:
            pass
        elif p.shares in best and p.cash > best[p.shares].cash:
            best[p.shares] = p
        elif not p.shares in best:
            best[p.shares] = p
    return list(best.values())


def transactions_to_orders(transactions, prices, symbol):
    order = pd.Series("", index=prices.index)
    shares = pd.Series(0, index=prices.index)

    for i, t in enumerate(transactions):
        if t > 0:
            order.iloc[i] = "BUY"
            shares.iloc[i] = t
        if t < 0:
            order.iloc[i] = "SELL"
            shares.iloc[i] = -t

    prices["Symbol"] = pd.Series(symbol, index=prices.index)
    prices["Order"] = order
    prices["Shares"] = shares
    prices.drop(columns=[symbol], inplace=True)
    prices = prices[shares != 0]
    return prices


def testPolicy(symbol, sd, ed, sv):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices.drop(columns=["SPY"], inplace=True)

    positions = [Position(sv, 0, [])]
    for date, price in prices.iterrows():
        positions = new_positions(positions, price[0])

    price = prices.iloc[-1][symbol]
    best_position = max(positions, key=lambda p: p.cash + p.shares * price)
    return transactions_to_orders(best_position.transactions, prices, symbol)


# def author():
#     return 'mkurale3'
#
# def testPolicy(symbol=”AAPL”, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
#     pricesDF= get_data([symbol],pd.date_range(sd, ed))
#     pricesDF= prices.fillna(method= "ffill").fillna(method= "bfill")
#     pricesDF.drop(columns=["SPY"], inplace=True)
#
#     positions = []
#     init_pos = (sv, 0, []) #cash, shares, [transactions]
#     positions = init_pos
#
#     additional_pos = []
#     for i in range(len(pricesDF)):
#         price = pricesDF.iloc[i, 0]
#         for pos in positions:
#             for orders in [-2000, -1000, 0, 1000, 2000]:
#                 new_cash_holding = pos[0] - orders*price
#                 newOrder_transactions = pos[2] + [orders]
#                 new_shares = pos[1] + orders
#                 new_pos = (new_cash_holding, new_shares, newOrder_transactions)
#                 additional_pos.append(new_pos)
#
#         positions = determineBestPositions(additional_pos)
#     position_with_max_cash = max(positions, key=lambda pos: pos[0] + pos[1]*prices)
# def determineBestPositions(positions):
#
#     best_pos = {}
#     for pos in positions:
#         cash = pos[0]
#         numShares = pos[1]
#         transactions = pos[2]
#         if numShares not in [-1000, 0, 1000]:
#             continue
#         elif numShares in best_pos and cash > best_pos[numShares][0]:
#             best_pos[numShares] = pos
#         elif numShares not in best_pos:
#             best_pos[numShares] = pos
#
#     return list(best_pos.values())


    