import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from hotspot_analyzer import hotspot_analyser

path = "C:\\Users\kshub\\OneDrive\\Documents\\PET_phase_2\\Technical_Phase_Data\\technical_phase_data.csv"
df = pd.read_csv(path)

start_date, end_date = datetime(2020, 9, 1), datetime(2021, 3, 31)
print(hotspot_analyser(df,start_date,end_date,"Medellin",42,10))