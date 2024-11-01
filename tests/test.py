import pytest
import pandas as pd
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from DP_epidemiology.hotspot_analyzer import hotspot_analyzer 
from DP_epidemiology.mobility_analyzer import mobility_analyzer
from DP_epidemiology.pandemic_adherence_analyzer import pandemic_adherence_analyzer
from DP_epidemiology.contact_matrix import get_age_group_count_map, get_contact_matrix, get_pearson_similarity

# Load test data
path = "tests/test_data.csv"
df = pd.read_csv(path)


@pytest.fixture
def start_date():
    return datetime(2020, 10, 1)

@pytest.fixture
def end_date():
    return datetime(2020, 10, 10)

@pytest.fixture
def city():
    return "Bogota"


def test_hotspot_analyzer(start_date, end_date, city):
    result = hotspot_analyzer(df, start_date, end_date, city, epsilon=10)
    
    # The output is a pandas DataFrame...
    assert isinstance(result, pd.DataFrame), "hotspot_analyzer did not return a DataFrame"
    
    # ... with two columns named nb_transactions and merch_postal_code...
    expected_columns = {"nb_transactions", "merch_postal_code"}
    assert set(result.columns) == expected_columns, f"Expected columns {expected_columns}, but got {set(result.columns)}"
    
    # ... and the nb_transactions column contains only non-negative numbers
    assert (result["nb_transactions"] >= 0).all(), "Column 'nb_transactions' contains negative numbers"


def test_mobility_analyzer(start_date, end_date, city):
    result = mobility_analyzer(df, start_date, end_date, city, epsilon=10)
    
    # The output is a pandas DataFrame...
    assert isinstance(result, pd.DataFrame), "mobility_analyzer did not return a DataFrame"
    
    # ... with two columns named nb_transactions and merch_postal_code...
    expected_columns = {"nb_transactions", "date"}
    assert set(result.columns) == expected_columns, f"Expected columns {expected_columns}, but got {set(result.columns)}"
    
    # ... where the nb_transactions column contains only non-negative numbers...
    assert (result["nb_transactions"] >= 0).all(), "Column 'nb_transactions' contains negative numbers"

    # ... and the date column contains only dates within the specified range
    assert pd.api.types.is_datetime64_any_dtype(result["date"]), "Column 'date' is not of type datetime"
    assert (result["date"] >= start_date).all(), "Column 'date' contains dates before the start date"
    assert (result["date"] <= end_date).all(), "Column 'date' contains dates after the end date"


def test_pandemic_adherence_analyzer(start_date, end_date, city):
    result = pandemic_adherence_analyzer(df, start_date, end_date, city, essential_or_luxury="luxury", epsilon=10)

    # The output is a pandas DataFrame...
    assert isinstance(result, pd.DataFrame), "pandemic_adherence_analyzer did not return a DataFrame"
    
    # ... with two columns named nb_transactions and merch_postal_code...
    expected_columns = {"nb_transactions", "date"}
    assert set(result.columns) == expected_columns, f"Expected columns {expected_columns}, but got {set(result.columns)}"
    
    # ... where the nb_transactions column contains only non-negative numbers...
    assert (result["nb_transactions"] >= 0).all(), "Column 'nb_transactions' contains negative numbers"

    # ... and the date column contains only dates within the specified range
    assert pd.api.types.is_datetime64_any_dtype(result["date"]), "Column 'date' is not of type datetime"
    assert (result["date"] >= start_date).all(), "Column 'date' contains dates before the start date"
    assert (result["date"] <= end_date).all(), "Column 'date' contains dates after the end date"

@pytest.fixture
def contact_matrix_params():
    return {
        "age_groups": ["20-30", "30-40", "40-50"],
        "consumption_distribution": {
            'Airlines': [25, 40, 15],
            'Bars/Discotheques': [50, 35, 15],
            'Hospitals': [15, 20, 30],
            'Drug Stores/Pharmacies': [15, 20, 30],
            'Computer Network/Information Services': [40, 35, 20],
            'General Retail Stores': [20, 35, 25],
            'Grocery Stores/Supermarkets': [20, 35, 25],
            'Utilities: Electric, Gas, Water': [15, 30, 30],
            'Hotels/Motels': [20, 25, 30],
            'Restaurants': [25, 25, 25]
        }
    }

def test_contact_matrix(contact_matrix_params, start_date, end_date, city):
    params = contact_matrix_params
    result = get_age_group_count_map(
        df, 
        contact_matrix_params["age_groups"], 
        contact_matrix_params["consumption_distribution"],
        start_date, end_date, city, 
        epsilon=1.0
    )

    # The output is a dictionary...
    assert isinstance(result, dict), "contact_matrix did not return a dictionary"
    
    # ... with keys matching the input age groups...
    assert list(result.keys()) == contact_matrix_params["age_groups"], f"Age groups in result contact matrix did not match input age groups"
    
    # ... and only positive values
    assert all(v >= 0 for v in result.values()), "Column 'nb_transactions' contains negative numbers"
