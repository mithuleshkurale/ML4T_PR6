import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt
import TheoreticallyOptimalStrategy as tos
import marketsimcode as ms
import indicators as indicators


def author():
    return 'mkurale3'


def createTableTOSPerfMetrics(portvals):
    daily_ret = (portvals / portvals.shift(1)) - 1
    cum_ret = (portvals[-1] / portvals[0]) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()

    data = {'cumulative return': [cum_ret], 'avg daily return': [avg_daily_ret], 'std daily return': [std_daily_ret]}
    metrics_df = pd.DataFrame(data)
    metrics_df.to_html('p6_results.html')


def createTableBenchMarkPerfMatrics(port_vals_benchmark):
    daily_ret_benchmark = (port_vals_benchmark / port_vals_benchmark.shift(1)) - 1
    cum_ret_benchmark = (port_vals_benchmark[-1] / port_vals_benchmark[0]) - 1
    avg_daily_ret_benchmark = daily_ret_benchmark.mean()
    std_daily_ret_benchmark = daily_ret_benchmark.std()

    data = {'cumulative return': [cum_ret_benchmark], 'avg daily return': [avg_daily_ret_benchmark],
            'std daily return': [std_daily_ret_benchmark]}
    metrics_df = pd.DataFrame(data)
    metrics_df.to_html('p6_results.html')


def compute_stats():
    df_trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    portvals = ms.compute_portvals(df_trades, symbol="JPM", startDate=dt.datetime(2008, 1, 1),
                                   endDate=dt.datetime(2009, 12, 31), start_val=100000, commission=0, impact=0)
    port_vals_normalized = portvals / portvals[0]

    benchMarkTrades_DF = tos.benchMark(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    port_vals_benchmark = ms.compute_portvals(benchMarkTrades_DF, symbol="JPM", startDate=dt.datetime(2008, 1, 1),
                                              endDate=dt.datetime(2009, 12, 31), start_val=100000, commission=0,
                                              impact=0)
    port_vals_benchmark_normalized = port_vals_benchmark / port_vals_benchmark[0]

    # generate chart
    df_temp = pd.concat([port_vals_normalized, port_vals_benchmark_normalized],
                        keys=['Theo Optimal Portfolio Normalized', 'Benchmark Normalized'], axis=1)
    df_temp.plot(title="Optimal Portfolio Normalized vs Benchmark Normalized", fontsize=12)
    plt.savefig('Figure1.png')
    plt.show()
    plt.clf()

    # generate table
    createTableTOSPerfMetrics(portvals)
    createTableBenchMarkPerfMatrics(port_vals_benchmark)


if __name__ == "__main__":
    compute_stats()
    indicators.run()
