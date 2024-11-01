from DP_epidemiology.utilities import *
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp
import matplotlib.pyplot as plt

dp.enable_features("contrib", "floating-point", "honest-but-curious")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


time_col = "date"
city_col = "city"

def validate_input_data(df, age_groups, consumption_distribution, start_date: datetime, end_date: datetime, city: str):
    # check city exists in the data
    df = make_preprocess_location()(df)
    df[time_col] = pd.to_datetime(df[time_col])
    if city not in df[city_col].unique():
        raise ValueError("City does not exist in the data")
    # check start date is not beyong the latest date and end date is not before the starting date in the data
    if start_date < df[time_col].min() or end_date > df[time_col].max():
        raise ValueError("Start date or end date is beyond the data range")
    # make sure all the categories in consumption distribution are present in the data
    merch_categories = df["merch_category"].unique()
    for category in consumption_distribution.keys():
        if category not in merch_categories:
            raise ValueError(f"Category {category} does not exist in the data")

    
def get_age_group_count_map(df, age_groups, consumption_distribution, start_date: datetime, end_date: datetime, city: str, epsilon: float = 1.0):

    validate_input_data(df, age_groups, consumption_distribution, start_date, end_date, city)

    # use the maximum number of transactions from each merchant category to clamp
    # assumption: this will be used for the unseen data
    clamp_window_nb_transactions = df.groupby("merch_category").agg(
        {"nb_transactions": "max"})["nb_transactions"].to_dict()

    t_pre = (
        make_preprocess_location()
        >> make_truncate_time(start_date, end_date, "date")
        >> make_filter_rows("transaction_type", "OFFLINE")
        >> make_filter_rows(city_col, city)
        # >> make_filter_rows_with_country("merch_postal_code", pincode_prefix)
    )
    number_of_timesteps = 1 if end_date == start_date else (
        end_date - start_date).days // 7
    input_space = dp.vector_domain(
        dp.atom_domain(T=int)), dp.symmetric_distance()
    df_new = t_pre(df)
    zip_code_list = df_new["merch_postal_code"].unique().astype(int)
    count_meas = input_space >> dp.t.then_count() >> dp.m.then_laplace(
        (3 * number_of_timesteps)/epsilon)
    dp_count = count_meas(zip_code_list)

    # Calculate the average number of transactions in each zip code for each merchant category during the given week.
    nb_transactions_avg_count_map = {}

    for category, upper_bound in clamp_window_nb_transactions.items():
        m_count = (
            t_pre
            # TODO: The scale has to be equal to bound/epsilon, which can be equal to the mean itself in cases where number of entries
            # per merch_category is like less than 5
            # but since the data will be disjoint after doing group by with merch_category, the epsilon will be the maximum of all the epsilons
            # If needed, take epsilon to be 10 for the category where bound is maximum of all
            >> make_private_nb_transactions_avg_count(merch_category=category, upper_bound=upper_bound, dp_dataset_size=dp_count, scale=(3*upper_bound*number_of_timesteps)/epsilon)
        )
        # print(category,":", m_count(df))
        nb_transactions_avg_count_map[category] = m_count(df)

    # calculate age group to avg count of members from that age group
    age_group_count_map = {}
    for age_group in age_groups:
        age_group_count_map[age_group] = max(np.sum([(proportion_list[age_groups.index(age_group)]/100)*nb_transactions_avg_count_map[category]
                                                 for category, proportion_list in consumption_distribution.items()]), 0)
   

    return age_group_count_map


def get_contact_matrix(sample_distribution, population_distribution):
    size = len(sample_distribution)
    C = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            C[i][j] = sample_distribution[i]

    M = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            M[i][j] = C[i][j]/sample_distribution[j]

    T = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            T[i][j] = M[i][j]*population_distribution[j]

    T = (T+np.transpose(T))/2

    F = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            F[i][j] = T[i][j]/population_distribution[j]

    return 2.8*F


def get_pearson_similarity(contact_matrix, Ground_truth_contact_matrix):
    Ground_truth_contact_matrix = [
        [3.91155, 3.84487, 3.32271],
        [2.12514, 2.77554, 3.19146],
        [2.15473, 2.34549, 2.70081]
    ]
    # Calculate the Pearson similarity between the ground truth contact matrix and the contact matrix
    pearson_similarity = np.corrcoef(np.array(
        Ground_truth_contact_matrix).flatten(), np.array(contact_matrix).flatten())[0, 1]
    return pearson_similarity

def plot_difference(A, B):
    difference = A - B

    plt.figure(figsize=(10, 8))
    plt.imshow(difference, cmap='coolwarm', interpolation='none')
    plt.colorbar(label='Difference')
    plt.title('Difference between estimated_C and contact_others')
    plt.xlabel('Index i2')
    plt.ylabel('Index i1')
    plt.show()

