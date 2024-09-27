import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DP_epidemiology.utilities import *

def get_age_group_count_map(path, start_date:datetime,end_date:datetime, pincode_prefix, epsilon:float=1.0):
    df = pd.read_csv(path)
    time_col = "date"
    # use the maximum number of transactions from each merchant category to clamp
    # assumption: this will be used for the unseen data
    clamp_window_nb_transactions = df.groupby("merch_category").agg(
        {"nb_transactions": "max"})["nb_transactions"].to_dict()
    
    t_pre = (
    make_truncate_time(start_date, end_date, "date")
    >> make_filter_rows("transaction_type", "OFFLINE")
    >> make_filter_rows_with_country("merch_postal_code", pincode_prefix)
)

    input_space = dp.vector_domain(
        dp.atom_domain(T=float)), dp.symmetric_distance()
    df[time_col] = pd.to_datetime(df[time_col])
    zip_code_list = df[(df["merch_postal_code"].astype(str).str.startswith(pincode_prefix))& (df[time_col] >=start_date) & (df[time_col] <= end_date)&(df["transaction_type"]=="OFFLINE")]["merch_postal_code"].unique()
    # (where TIA stands for Atomic Input Type)
    # TODO: what should be the sensitivity here? Many merchant records can contribute to the same zip code
    # So, scale = 1, is a good enough choice.
    count_meas = input_space >> dp.t.then_count() >> dp.m.then_laplace(1.)
    dp_count = count_meas(zip_code_list)

    # Calculate the average number of transactions in each zip code for each merchant category during the given week.
    nb_transactions_avg_count_map = {}
    number_of_timesteps = 1 if end_date == start_date else (end_date - start_date).days // 7
    for category, upper_bound in clamp_window_nb_transactions.items():
        m_count = (
            t_pre
            # TODO: The scale has to be equal to bound/epsilon, which can be equal to the mean itself in cases where number of entries
            # per merch_category is like less than 5
            # but since the data will be disjoint after doing group by with merch_category, the epsilon will be the maximum of all the epsilons
            # If needed, take epsilon to be 10 for the category where bound is maximum of all
            >> make_private_nb_transactions_avg_count(merch_category = category, upper_bound = upper_bound, dp_dataset_size = dp_count, zip_code_list = zip_code_list,  scale = (3*upper_bound*number_of_timesteps)/epsilon)
        )
        # print(category,":", m_count(df))
        nb_transactions_avg_count_map[category] = m_count(df)

    # Proportion of age groups ie 20-30, 30-40, 40-50 involved in any merhcandise category
    age_group_proportion_map = {
    'Airlines': [25, 40, 15],
    'Bars/Discotheques': [50, 35, 15],
    'Hospitals' : [15, 20, 30],
    'Drug Stores/Pharmacies' : [15, 20, 30 ],
    'Computer Network/Information Services': [40, 35, 20],
    'General Retail Stores': [20, 35, 25],
    'Grocery Stores/Supermarkets': [20, 35, 25],
    'Utilities: Electric, Gas, Water': [15, 30, 30],
    'Hotels/Motels': [20, 25, 30],
    'Restaurants': [25, 25, 25]
    }
    # calculate age group to avg count of members from that age group
    age_group_count_map = {}
    age_group_count_map["20-30"] = np.sum([ (proportion_list[0]/100)*nb_transactions_avg_count_map[category] for category, proportion_list in age_group_proportion_map.items()]) # Call np.sum() on the list comprehension result
    age_group_count_map["30-40"] = np.sum([ (proportion_list[1]/100)*nb_transactions_avg_count_map[category] for category, proportion_list in age_group_proportion_map.items()]) # Call np.sum() on the list comprehension result
    age_group_count_map["40-50"] = np.sum([ (proportion_list[2]/100)*nb_transactions_avg_count_map[category] for category, proportion_list in age_group_proportion_map.items()]) # Call np.sum() on the list comprehension result

    return age_group_count_map