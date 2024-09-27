import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DP_epidemiology.utilities import *

def pandemic_stage_analyzer(df:pd.DataFrame,start_date:datetime,end_date:datetime,city: str,essential_or_luxury:str, epsilon:float):
    """final function to predict hotspots"""
    bounds = (0, 600)
    transaction_data_col = "nb_transactions"
    groupby_col = "date"

    city_col="city"
    time_col="date"
    merch_category_col="merch_super_category"


    """time steps calculation"""
    nb_timesteps = (end_date - start_date).days // 7

    """scale calculation"""
    scale=(np.sqrt(3.0)*nb_timesteps)/epsilon

    new_df=df.copy()


    hotspot_predictor=(
    make_preprocess_location()
    >>make_preprocess_merchant()
    >>make_filter(city_col,city)
    >>make_filter(merch_category_col,essential_or_luxury)
    >>make_truncate_time(start_date, end_date, time_col)
    >>make_private_sum_by(transaction_data_col, groupby_col, bounds, scale)
   )

    return hotspot_predictor(new_df)