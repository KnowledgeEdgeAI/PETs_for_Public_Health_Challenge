import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import scipy.stats as stats
import opendp.prelude as dp
import matplotlib.pyplot as plt
from dtw import dtw,accelerated_dtw

dp.enable_features("contrib", "floating-point", "honest-but-curious")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DP_epidemiology.utilities import *

def mobility_analyzer_airline(df:pd.DataFrame,start_date:datetime,end_date:datetime,city: str, epsilon:float):
    """final function to predict hotspots"""
    bounds = (0, 600)
    upper_bound=600
    transaction_data_col = "nb_transactions"
    groupby_col = "date"

    city_col="city"
    time_col="date"
    merch_category_col="merch_category"
    merch_filter="Airlines"
    

    """time steps calculation"""
    nb_timesteps = (end_date - start_date).days // 7

    """scale calculation"""
    scale=(np.sqrt(3.0)*nb_timesteps*upper_bound)/epsilon

    new_df=df.copy()


    analyzer=(
    make_preprocess_location()
    >>make_filter(city_col,city)
    >>make_filter(merch_category_col,merch_filter)
    >>make_truncate_time(start_date, end_date, time_col)
    >>make_private_sum_by(transaction_data_col, groupby_col, bounds, scale)
   )

    return analyzer(new_df)

def mobility_analyzer(df:pd.DataFrame,start_date:datetime,end_date:datetime,city: str,category:str, epsilon:float):
    """final function to predict hotspots"""
    bounds = (0, 600)
    upper_bound=600
    transaction_data_col = "nb_transactions"
    groupby_col = "date"

    city_col="city"
    time_col="date"
    merch_category_col="merch_super_category"
    # merch_filter="Airlines"
    

    """time steps calculation"""
    nb_timesteps = (end_date - start_date).days // 7

    """scale calculation"""
    scale=(np.sqrt(3.0)*nb_timesteps*upper_bound)/epsilon

    new_df=df.copy()


    analyzer=(
    make_preprocess_location()
    >>make_preprocess_merchant_mobility()
    >>make_filter(city_col,city)
    >>make_filter(merch_category_col, category)
    >>make_truncate_time(start_date, end_date, time_col)
    >>make_private_sum_by(transaction_data_col, groupby_col, bounds, scale)
   )

    return analyzer(new_df)

def mobility_validation_with_google_mobility(df_transactional_data:pd.DataFrame, df_google_mobility_data:pd.DataFrame, start_date:datetime, end_date:datetime, city:str, category:str, epsilon:float):
    df_transactional_mobility= mobility_analyzer(df_transactional_data,start_date,end_date,city,category,epsilon)
    offset=df_transactional_mobility["date"][0]
    df_google_mobility = preprocess_google_mobility(df_google_mobility_data,start_date,end_date,city,category,offset)

    length =min(len(df_transactional_mobility),len(df_google_mobility))
    # print(df_transactional_mobility.head())
    # print(df_google_mobility.head())
    r, p = stats.pearsonr(df_transactional_mobility['nb_transactions'][:length], df_google_mobility[category][:length])
    print(f"Scipy computed Pearson r: {r} and p-value: {p}")

    d1 = df_transactional_mobility[category][:length].interpolate().values
    d2 = df_google_mobility[category][:length].interpolate().values
    d, cost_matrix, acc_cost_matrix, path = accelerated_dtw(d1,d2, dist='euclidean')

    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.xlabel('Subject1')
    plt.ylabel('Subject2')
    plt.title(f'DTW Minimum Path with minimum distance: {np.round(d,2)}')
    plt.show()