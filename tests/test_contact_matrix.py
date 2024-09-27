import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from DP_epidemiology.contact_matrix import get_age_group_count_map

path = "C:\\Users\kshub\\OneDrive\\Documents\\PET_phase_2\\Technical_Phase_Data\\technical_phase_data.csv"
df = pd.read_csv(path)

week = "2022-12-27"
pincode_prefix = "70"
print(get_age_group_count_map(path, week, pincode_prefix))