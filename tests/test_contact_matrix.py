import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from DP_epidemiology.contact_matrix import get_age_group_count_map, get_contact_matrix

path = "C:\\Users\\Milan Anand Raj\\Desktop\\KNOWLEDGEEDGEAI\\PET\\pets_mockdata\\Technical_Phase_Data\\technical_phase_data.csv"
df = pd.read_csv(path)

print("contact_matrix")
start_date, end_date = datetime(2022,12,27), datetime(2022,12,27)
pincode_prefix = "70"
age_group_count_map = get_age_group_count_map(path, start_date, end_date, pincode_prefix)
age_group_sample_size = list(age_group_count_map.values())
age_group_population_distribution =  [8231200, 7334319, 6100177]
print(get_contact_matrix(age_group_sample_size, age_group_population_distribution))
