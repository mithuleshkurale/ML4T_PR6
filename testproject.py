import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt
import TheoreticallyOptimalStrategy as tos
import marketsimcode as ms
import indicators as indicators


def author():
    return 'mkurale3'


def createTableTOSAndBenchmarkPerfMetrics(portvals, port_vals_benchmark):
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        raise Exception("warning, code did not return a DataFrame")

    daily_ret = (portvals / portvals.shift(1)) - 1
    cum_ret = (portvals[-1] / portvals[0]) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()

    cum_ret = "{:.6}".format(cum_ret)
    avg_daily_ret = "{:.6}".format(avg_daily_ret)
    std_daily_ret = "{:.6}".format(std_daily_ret)

    data = {'cumulative return': [cum_ret], 'avg daily return': [avg_daily_ret], 'std daily return': [std_daily_ret]}
    metrics_df = pd.DataFrame(data)
    # metrics_df.to_html('p6_results.html')

    if isinstance(port_vals_benchmark, pd.DataFrame):
        port_vals_benchmark = port_vals_benchmark[port_vals_benchmark.columns[0]]  # just get the first column
    else:
        raise Exception("warning, code did not return a DataFrame")

    daily_ret_benchmark = (port_vals_benchmark / port_vals_benchmark.shift(1)) - 1
    cum_ret_benchmark = (port_vals_benchmark[-1] / port_vals_benchmark[0]) - 1
    avg_daily_ret_benchmark = daily_ret_benchmark.mean()
    std_daily_ret_benchmark = daily_ret_benchmark.std()

    cum_ret_benchmark = "{:.6}".format(cum_ret_benchmark)
    avg_daily_ret_benchmark = "{:.6}".format(avg_daily_ret_benchmark)
    std_daily_ret_benchmark = "{:.6}".format(std_daily_ret_benchmark)
    data_benchmark = {'cumulative return': [cum_ret_benchmark], 'avg daily return': [avg_daily_ret_benchmark],
                      'std daily return': [std_daily_ret_benchmark]}
    bench_df = pd.DataFrame(data_benchmark)

    df_temp = pd.concat([metrics_df, bench_df], axis=0)
    df_temp['Type'] = (['TOS', 'Bench'])
    first_col = df_temp.pop('Type')
    df_temp.insert(0, 'Type', first_col)
    df_temp.to_csv('p6_results.txt', index=False)


def generate_tos_benchmark_graph(port_vals_normalized, port_vals_benchmark_normalized):
    df_temp = pd.concat([port_vals_normalized, port_vals_benchmark_normalized],
                        keys=['Theo Optimal Portfolio Normalized', 'Benchmark Normalized'], axis=1)
    ax = df_temp.plot(kind='line', y='Theo Optimal Portfolio Normalized', color='red')
    df_temp.plot(kind='line', y='Benchmark Normalized', color='purple', ax=ax)
    plt.title("TOS Normalized vs Benchmark Normalized")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Values")
    plt.legend(['TOS', 'Benchmark'])
    plt.savefig('Figure1.png')
    # plt.show()
    plt.close()


def compute_stats():
    df_trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    portvals = ms.compute_portvals(df_trades, symbols=["JPM"], startDate=dt.datetime(2008, 1, 1),
                                   endDate=dt.datetime(2009, 12, 31), start_val=100000, commission=0, impact=0)
    port_vals_normalized = portvals / portvals.iloc[0, 0]

    benchMarkTrades_DF = tos.benchMark(symbol=["JPM"], sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    port_vals_benchmark = ms.compute_portvals(benchMarkTrades_DF, symbols=["JPM"], startDate=dt.datetime(2008, 1, 1),
                                              endDate=dt.datetime(2009, 12, 31), start_val=100000, commission=0,
                                              impact=0)
    port_vals_benchmark_normalized = port_vals_benchmark / port_vals_benchmark.iloc[0, 0]

    # generate chart
    generate_tos_benchmark_graph(port_vals_normalized, port_vals_benchmark_normalized)

    # generate table
    createTableTOSAndBenchmarkPerfMetrics(portvals, port_vals_benchmark)


if __name__ == "__main__":
    compute_stats()
    indicators.run()
