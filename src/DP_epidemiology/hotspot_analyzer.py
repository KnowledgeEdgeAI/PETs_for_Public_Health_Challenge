import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DP_epidemiology.utilities import *

def hotspot_analyzer(df:pd.DataFrame,city_zipcode_map:pd.DataFrame, start_date:datetime,end_date:datetime,city:str, default_city:str, epsilon:float):
    """final function to predict hotspots"""
    bounds = (0, 600)
    upper_bound=600
    transaction_data_col = "nb_transactions"
    postal_code_groupby_col = "merch_postal_code"
    transaction_type_col = "transaction_type"
    transaction_type_filter = "OFFLINE"
    city_col="city"
    time_col="date"
    
    """time steps calculation"""
    nb_timesteps = (end_date - start_date).days // 7

    """scale calculation"""
    scale=(3.0*nb_timesteps*upper_bound)/epsilon

    new_df=df.copy()


    hotspot_predictor=(
    make_preprocess_location(city_zipcode_map, default_city)
    >>make_filter(transaction_type_col,transaction_type_filter)
    >>make_filter(city_col,city)
    >>make_truncate_time(start_date, end_date, time_col)
    >>make_private_sum_by(transaction_data_col, postal_code_groupby_col, bounds, scale)
   )

    return hotspot_predictor(new_df)
    
if __name__ == "__main__":
    import sys
    path=sys.argv[1]
    path_city_zipcode_map=sys.argv[2]
    start_date=datetime(sys.argv[3])
    end_date=datetime(sys.argv[4])
    city=sys.argv[5]
    default_city=sys.argv[6]
    epsilon=sys.argv[7]
    df = pd.read_csv(path)
    city_zipcode_map = pd.read_csv(path_city_zipcode_map)
    print(hotspot_analyzer(df,city_zipcode_map, start_date,end_date,city,default_city, epsilon))