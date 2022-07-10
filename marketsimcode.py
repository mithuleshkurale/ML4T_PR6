""""""
import math

"""MC2-P1: Market simulator.  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Atlanta, Georgia 30332  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
All Rights Reserved  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

Template code for CS 4646/7646  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
and other users of this template code are advised not to share it with others  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
or edited.  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

We do grant permission to share solutions privately with non-students such  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
as potential employers. However, sharing with other current or future  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT honor code violation.  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

-----do not edit anything above this line---  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 

Student Name: Mithulesh Kurale  		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT User ID: mkurale3   		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT ID: 903081123   		  	   		  	  			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
"""

import datetime as dt
import numpy as np
import pandas as pd
from util import get_data


def author():
    return 'mkurale3'


def compute_portvals(
        tradesMadeDF,
        symbols=["JPM"],
        startDate=dt.datetime(2008, 1, 1),
        endDate=dt.datetime(2009, 12, 31),
        start_val=1000000,
        commission=0,
        impact=0,
):
    """
    Computes the portfolio values.

    :param orders_file: Path of the order file or the file object
    :type orders_file: str or file object
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """

    pricesDF = get_data(symbols, pd.date_range(startDate, endDate))
    pricesDF["Cash"] = 1

    # Step 4: Populate the trades data frame
    tradesDF = populateTradesDataFrame(tradesMadeDF, pricesDF, commission, impact, symbols)

    # Step 5: Populate the holdings data
    holdingsDF = populateHoldingsDataFrame(tradesDF, start_val, symbols)
    portVals = computePortVals(pricesDF, holdingsDF)
    portVals = portVals.set_index('Date')

    return portVals


def computePortVals(pricesDF, holdingsDF):
    symbols = holdingsDF.columns[1:-1]
    holdingsDF["PortVal"] = 0

    for i in range(len(holdingsDF)):
        # for each row in orders fetch the column data
        val = 0
        date = holdingsDF.loc[i, "Date"]
        cash = holdingsDF.loc[i, "Cash"]

        for sym in symbols:
            val = val + (pricesDF.loc[date, sym] * holdingsDF.loc[i, sym])
        val += cash
        holdingsDF.loc[i, "PortVal"] = val

    return holdingsDF[["Date", "PortVal"]]


def populateTradesDataFrame(tradesMadeDF, pricesDF, commission, impact, symbols):
    col_names = ["Date", "Cash"]
    col_names.extend(symbols)
    tradesDataFrame = pd.DataFrame(np.zeros((len(pricesDF), len(col_names))), columns=col_names)
    tradesDataFrame['Date'] = pricesDF.index
    tradesDataFrame["Cash"] = 0
    symbol = symbols[0]
    for date, row in tradesMadeDF.iterrows():
        # for each row in orders fetch the column data
        shares_traded = row['Trades']

        # if buy order than for specific date add to existing shares of certain stock

        stockPrice = pricesDF.loc[date, symbol]

        if shares_traded > 0:  # BUY
            currCashEarnings = ((stockPrice * shares_traded * (-1 - impact)) - commission)
        elif shares_traded < 0:  # SELL
            currCashEarnings = (stockPrice * abs(shares_traded) * (1 - impact)) - commission
        elif shares_traded == 0:  # DO Nothing
            currCashEarnings = 0
        else:
            raise Exception("Unidentifiable order type")
        tradesDataFrame.loc[tradesDataFrame['Date'] == date, symbol] += shares_traded
        tradesDataFrame.loc[tradesDataFrame['Date'] == date, "Cash"] += currCashEarnings

    return tradesDataFrame


def createNewRowToInsert(tradesOnDate_DF, symbols, date):
    totalCashEarningsOnTradeDate = tradesOnDate_DF["Cash"].sum()
    shareCountForEachStock = []
    newRowToAppend = []
    for sym in symbols:
        shareCount = tradesOnDate_DF[sym].sum()
        shareCountForEachStock.append(shareCount)
    newRowToAppend.extend([date, totalCashEarningsOnTradeDate])
    newRowToAppend.extend(shareCountForEachStock)

    return newRowToAppend


def populateHoldingsDataFrame(tradesDataFrame, start_val, symbols):
    col_names = ["Date", "Cash"]
    col_names.extend(symbols)
    holdingsDataFrame = pd.DataFrame(columns=col_names)
    holdingsDataFrame.loc[len(holdingsDataFrame)] = 0

    holdingsDataFrame.loc[0, "Cash"] = start_val

    # populate the first row of holdings according to the trades holding
    date_set = set([])
    date = tradesDataFrame.loc[0, "Date"]
    date_set.add(date)
    holdingsDataFrame.iloc[0, 0] = date
    tradesOnDate_DF = tradesDataFrame.loc[tradesDataFrame["Date"] == date]
    newRow = createNewRowToInsert(tradesOnDate_DF, symbols, date)
    # create a df from new row
    newRowDf = pd.DataFrame(newRow).T
    newRowDf.columns = col_names

    holdingsDataFrame.iloc[0, 1:] = holdingsDataFrame.iloc[0, 1:] + newRowDf.iloc[0, 1:]

    # populate
    currIndex = len(holdingsDataFrame)
    for i in range(1, len(tradesDataFrame)):
        # parse out the date
        date = tradesDataFrame.loc[i, "Date"]
        if date in date_set:
            continue
        date_set.add(date)
        tradesOnDate_DF = tradesDataFrame.loc[tradesDataFrame["Date"] == date]
        newRow = createNewRowToInsert(tradesOnDate_DF, symbols, date)
        newRowDf = pd.DataFrame(newRow).T
        newRowDf.columns = col_names

        holdingsDataFrame.loc[currIndex] = holdingsDataFrame.iloc[currIndex - 1, 1:] + newRowDf.iloc[0, 1:]
        holdingsDataFrame.loc[currIndex, "Date"] = date
        currIndex += 1

    cashCol = holdingsDataFrame.pop("Cash")
    holdingsDataFrame.insert(len(holdingsDataFrame.columns), "Cash", cashCol)

    return holdingsDataFrame
