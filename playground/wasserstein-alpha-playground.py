import random
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance
from scipy.stats import norm
import ot
import matplotlib.pyplot as plt
import requests

def main():
    indices = ['^GSPC', '^IXIC']
    companies = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']
    tickers = indices + companies
    
    '''
    1d: 10-15 years
    60m: 2 years (730 days)
    30m: 60 days
    '''
    start_date = '2021-05-01'
    end_date = '2023-04-20'
    interval = '60m'
    win_size=7
    stock_data = yf.download(tickers, start=start_date, end=end_date, interval=interval)
    for ticker in tickers:
        stock_data[('Average', ticker)] = (stock_data[('High', ticker)] + stock_data[('Low', ticker)]) / 2
        stock_data[('Rolling Avg', ticker)] = stock_data[('Average', ticker)].rolling(window=win_size).mean()
    
    
    # Group stock price data by date by aggregating averages between High and Low for every 60m.
    # Add a new column with a list that has normalized prices.
    agg_df = stock_data.groupby(pd.Grouper(freq='D')).agg(list)
    for ticker in tickers:
        agg_df[('Average Norm', ticker)] = agg_df[('Average', ticker)].apply(lambda x: [v/np.sum(x) for v in x])
    # print(agg_df.loc[:, (slice(None), 'GOOGL')])
    print('GOOGL stock_data: \n', stock_data.loc[:, (slice(None), 'GOOGL')])
    
    
    # Compute Gromov-Wasserstein barycenter on the distributions of daily data
    barycenter_win_size = 7
    for ticker in tickers:
        # TODO: Move dropping of rows to stock_data dropping the empty price rows
        mask = agg_df[('Average Norm', ticker)].apply(lambda x: len(x) < win_size)
        agg_df = agg_df[~mask]
        df_data = agg_df[('Average Norm', ticker)]
        barycenters = [-1] * barycenter_win_size
        for i in range(barycenter_win_size, len(agg_df)):
            prev_distr = np.stack(df_data.iloc[i-barycenter_win_size: i].values)
            first_distr = np.array(df_data.iloc[0])
            # cost_basis = np.array(first_distr)
            # M = ot.dist(cost_basis, cost_basis)                                 # First distribution available as cost basis
            M = np.eye(len(agg_df[('Average Norm', ticker)][0]))                   # Identify matrix as cost basis
            weights = np.ones(len(prev_distr)) / len(prev_distr)
            barycenter = ot.bregman.barycenter(prev_distr.T, M, reg=0.01, weights=weights)
            barycenters.append(barycenter)
        barycenters_col = pd.Series(barycenters, name=('Barycenter', ticker), index=agg_df.index)
        agg_df = pd.concat([agg_df, barycenters_col], axis=1)
    print('GOOGL agg_df\n', agg_df.loc[:, (slice(None), 'GOOGL')])
    
    function = 'TIME_SERIES_INTRADAY_EXTENDED'
    symbol = 'GOOGL'
    apikey = '31MSI0X5E4NOZJ3J'
    interval = '15min'
    data_slice = 'year1month1'
    
    
    '''
    # ================================================================================================================
    # plot_data = stock_data.loc[:, (slice(None), 'GOOGL')]                                 # Plotting all columns for a given index
    # plot_data = stock_data.loc[:, [('Rolling Avg', 'GOOGL'), ('Average', 'GOOGL')]]       # Plotting select columns for a given index
    plot_data = stock_data['Rolling Avg']['GOOGL']
    fig, ax = plt.subplots(figsize=(12,6))
    plot_data.plot(ax=ax)
    plt.title(f"{tickers} Stock Price Data")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(loc="upper left")
    plt.show()
    # ================================================================================================================
    '''
    

if __name__ == '__main__':
    main()