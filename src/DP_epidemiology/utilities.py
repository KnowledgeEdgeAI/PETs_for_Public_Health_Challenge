import pandas as pd
import numpy as np
from datetime import datetime
import opendp.prelude as dp
import random

dp.enable_features("contrib", "floating-point", "honest-but-curious")



def dataframe_domain(public_key_sets=None):
    """Creates a domain representing the set of all data frames.
    
    Assumes column names and types are public information.
    Key sets optionally named for columns in `public_key_sets` are considered public information.

    Two data frames differing in their public information 
    are considered to have a data set distance of infinity.
    """
    return dp.user_domain(
        "DataFrameDomain", lambda x: isinstance(x, pd.DataFrame), public_key_sets
    )


def series_domain():
    """Creates a domain representing the set of all series.

    Assumes series name and type are public information.

    Two series differing in their public information 
    are considered to have a data set distance of infinity.
    """
    return dp.user_domain("SeriesDomain", lambda x: isinstance(x, pd.Series))

def identifier_distance():
    """Symmetric distance between the id sets."""
    return dp.user_distance("IdentifierDistance")


def approx_concentrated_divergence():
    """symmetric distance between the id sets"""
    return dp.user_distance("ApproxConcentratedDivergence()")

def make_preprocess_location():
    """Create a 1-stable transformation to bin `merch_postal_code` by city"""

    def categorize_city(code):
        if code.startswith("5"):
            return "Medellin"
        elif code.startswith("11"):
            return "Bogota"
        elif code.startswith("70"):
            return "Brasilia"
        else:
            return "Santiago"

    def location_preprocess(df):
        loc_df = df.copy()
        # Convert merchant_postal_code into str type
        loc_df["merch_postal_code"] = loc_df["merch_postal_code"].astype(str)
        # Apply the function to create a new column
        loc_df["city"] = loc_df["merch_postal_code"].apply(
            categorize_city
        )
        return loc_df

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=identifier_distance(),
        function=location_preprocess,
        stability_map=lambda d_in: d_in,
    )

def make_truncate_time(start_date, end_date, time_col):
    """Create a transformation that filters the data to a given time frame.
    
    WARNING: Assumes that the data has at most one contribution per individual per week.
    """
    number_of_timesteps = (end_date - start_date).days // 7

    def time_preprocess(df):
        df = df.copy()

        # Convert time_col into datetime type
        df[time_col] = pd.to_datetime(df[time_col])

        # Filter the DataFrame based on the specified dates
        return df[(df[time_col] >= start_date) & (df[time_col] <= end_date)]

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=dp.symmetric_distance(),
        function=time_preprocess,
        stability_map=lambda d_in: d_in * number_of_timesteps,
    )

def make_sum_by(column, by, bounds):
    """Create a transformation that computes the grouped bounded sum of `column`"""
    L, U = bounds
    def function(df):
        df = df.copy()
        df[column] = df[column].clip(*bounds)
        return df.groupby(by)[column].sum()

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_domain=series_domain(),
        output_metric=dp.l2_distance(T=float),
        function=function,
        stability_map=lambda d_in: np.sqrt(d_in) * max(abs(L), U),
    )


def make_private_sum_by(column, by, bounds, scale):
    """Create a measurement that computes the grouped bounded sum of `column`"""
    space = dp.vector_domain(dp.atom_domain(T=int)), dp.l1_distance(T=int)
    m_lap = space >> dp.m.then_laplace(scale)
    t_sum = make_sum_by(column, by, bounds)

    def function(df):
        exact = t_sum(df)
        # print(exact)
        noisy_sum = pd.Series(
            np.maximum(m_lap(exact.to_numpy().flatten()), 0), 
        )
        # print(noisy_sum)
        noisy_sum=noisy_sum.to_frame(name=column)
        noisy_sum[by] = exact.index
        return noisy_sum

    return dp.m.make_user_measurement(
        input_domain=dataframe_domain(public_key_sets=[by]),
        input_metric=dp.symmetric_distance(),
        output_measure=dp.zero_concentrated_divergence(T=float),
        function=function,
        privacy_map=lambda d_in: m_lap.map(t_sum.map(d_in)),
    )

def make_filter(column,entry):
        """filters offline entries"""
        
        def function(df):
            df = df.copy()
            return df[(df[column] == entry)]


        return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=identifier_distance(),
        function=function,
        stability_map=lambda d_in: d_in,
    )

def make_preprocess_merchant():
    """Create a 1-stable transformation to bin `merch_postal_code` by city"""

    def categorize_merchant(merch):
        if merch in ['Hotels/Motels','Restaurants','Bars/Discotheques']:
            return "luxury"
        elif merch in ['Grocery Stores/Supermarkets','Drug Stores/Pharmacies','General Retail Stores','Utilities: Electric, Gas, Water','Hospitals']:
            return "essential"
        else:
            return "other"

    def merchant_preprocess(df):
        loc_df = df.copy()
        # Convert merchant_postal_code into str type
        loc_df["merch_category"] = loc_df["merch_category"].astype(str)
        # Apply the function to create a new column
        loc_df["merch_super_category"] = loc_df["merch_category"].apply(
            categorize_merchant
        )
        return loc_df

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=identifier_distance(),
        function=merchant_preprocess,
        stability_map=lambda d_in: d_in,
    )

def get_coordinates(df:pd.DataFrame):
    postal_codes=df["merch_postal_code"].unique()


    postal_code = {
        'Medellin': [ code  for code in postal_codes if str(code).startswith('5')],
        'Bogota': [ code  for code in postal_codes if str(code).startswith('11')],
        'Brasilia': [ code  for code in postal_codes if str(code).startswith('70')],
        'Santiago': [ code  for code in postal_codes if not str(code).startswith('5') and not str(code).startswith('11') and not str(code).startswith('70')]
    }

    # Reference coordinates
    reference_coords = {
        "Medellin": (6.2476, -75.5658),
        "Bogota": (4.7110, -74.0721),
        "Brasilia": (-15.7975, -47.8919),
        "Santiago": (-33.4489, -70.6693)
    }

    # Function to generate unique coordinates
    def generate_unique_coords(base_lat, base_lon, num_coords):
        coords = []
        for _ in range(num_coords):
            # Slightly vary the base coordinates
            lat_variation = random.uniform(-1.5, +1.5)
            lon_variation = random.uniform(-1.5, +1.5)
            new_lat = base_lat + lat_variation
            new_lon = base_lon + lon_variation
            coords.append((new_lat, new_lon))
        return coords

    # Assign unique coordinates to each postal code
    postal_code_coords = {}
    for segment, codes in postal_code.items():
        base_lat, base_lon = reference_coords[segment]
        unique_coords = generate_unique_coords(base_lat, base_lon, len(codes))
        for code, coord in zip(codes, unique_coords):
            postal_code_coords[code] = coord

    df['Latitude'], df['Longitude'] = zip(*df['merch_postal_code'].map(postal_code_coords))
    return df


def make_filter_rows(column_name, value):
    """Create a transformation that filters the rows based on the value of a column `column_name`.

    """

    def filter_rows(df):
        df = df.copy()

        # Filter the rows
        return df[df[column_name] == value]

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_domain=dataframe_domain(),
        output_metric=dp.symmetric_distance(),
        function=filter_rows,
        stability_map=lambda d_in: d_in,
    )

def make_filter_rows_with_country(column_name, country_code_prefix):
    """Create a transformation that filters the rows based on the value of a column `column_name`.
    """
    def filter_rows(df):
        df = df.copy()

        # Filter the rows
        return df[df["merch_postal_code"].astype(str).str.startswith(country_code_prefix)]

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_domain=dataframe_domain(),
        output_metric=dp.symmetric_distance(),
        function=filter_rows,
        stability_map=lambda d_in: d_in,
    )

def make_private_nb_transactions_avg_count(merch_category, upper_bound , dp_dataset_size, scale = 1.0):
    """Create a measurement that computes the grouped bounded sum"""

    def compute_private_sum(df):
        df = df.copy()
        sum = df[df["merch_category"]==merch_category]["nb_transactions"].clip(lower=0, upper=upper_bound).sum()
        dp_sum = np.random.laplace(loc=sum, scale=scale)
        return dp_sum

    return dp.m.make_user_measurement(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_measure=dp.max_divergence(T=float),
        function=compute_private_sum,
        privacy_map=lambda d_in: d_in*upper_bound,
    )

def make_private_count(city_col, city, epsilon):
    """Create a measurement that computes the count of the unique zip codes in the given city"""

    def private_count(df):
        df = df.copy()
        zip_code_list = df[df[city_col]==city]["merch_postal_code"].unique()
        # (where TIA stands for Atomic Input Type)
        input_space = dp.vector_domain(dp.atom_domain(T=float)), dp.symmetric_distance()
        # (where TIA stands for Atomic Input Type)
        # TODO: what should be the sensitivity here? Many merchant records can contribute to the same zip code
        # So, scale = 1, is a good enough choice.
        count_meas = input_space >> dp.t.then_count() >> dp.m.then_laplace(1.)
        dp_count = count_meas(zip_code_list)
        return dp_count
    
    return dp.m.make_user_measurement(
        input_domain=dataframe_domain(),
        input_metric=dp.symmetric_distance(),
        output_measure=dp.max_divergence(T=int),
        function=private_count,
        privacy_map=lambda d_in: d_in*epsilon,
    )

def make_preprocess_merchant_mobility():
    """Create a 1-stable transformation to bin `merch_postal_code` by city"""

    def categorize_merchant(merch):
        if merch in ['General Retail Stores','Restaurants','Bars/Discotheques']:
            return "retail_and_recreation"
        elif merch in ['Grocery Stores/Supermarkets','Drug Stores/Pharmacies']:
            return "grocery_and_pharmacy"
        elif merch in ['Airlines']:
            return "transit_stations"
        else:
            return "other"

    def merchant_preprocess(df):
        loc_df = df.copy()
        # Convert merchant_postal_code into str type
        loc_df["merch_category"] = loc_df["merch_category"].astype(str)
        # Apply the function to create a new column
        loc_df["merch_super_category"] = loc_df["merch_category"].apply(
            categorize_merchant
        )
        return loc_df

    return dp.t.make_user_transformation(
        input_domain=dataframe_domain(),
        input_metric=identifier_distance(),
        output_domain=dataframe_domain(),
        output_metric=identifier_distance(),
        function=merchant_preprocess,
        stability_map=lambda d_in: d_in,
    )

def preprocess_google_mobility(df:pd.DataFrame,start_date:datetime, end_date:datetime,  city:str, category:str, offset: datetime=None):

    # df = df.copy()

    def region_filter(df, country_code, region_1, region_2, all=False):
        df=df.copy()
        mask = ((df["country_region_code"].isin(country_code)) & (df["sub_region_1"].isin(region_1)))
        if all:
            mask = (mask & (df["sub_region_2"].isin(region_2)))
        return df[mask]
    
    def time_preprocess(df):
        df = df.copy()

        # Filter the DataFrame based on the specified dates
        return df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    
    if city == "Bogota":
        df = region_filter(df, ["CO"], ["Bogota"], "")
    elif city == "Medellin":
        df = region_filter(df, ["CO"], ["Antioquia"], ["Medellin"], all=True)
    elif city == "Santiago":
        df = region_filter(df, ["CL"], ["Santiago Metropolitan Region"], ["Santiago Province"], all=True)
    elif city == "Brasilia":
        df = region_filter(df, ["BR"], ["Federal District"], "")
    else:
        raise ValueError("Invalid city")

    df = df.drop(["place_id", "country_region_code", "country_region", "sub_region_1", "sub_region_2", "metro_area", "iso_3166_2_code", "census_fips_code","parks_percent_change_from_baseline","workplaces_percent_change_from_baseline","residential_percent_change_from_baseline"], axis=1)
    
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    df=time_preprocess(df)
    # Set the date column as the index
    df.set_index('date', inplace=True)

    # Group by week and calculate the sum
    df_weekly = df.resample('W', label="right").sum()

    # Shift dates back to original dates
    if offset:
        
        if not (offset >= (df_weekly.index[0]-pd.DateOffset(7)) and  offset<=df_weekly.index[1]):
            raise ValueError("Invalid offset date")
        
        df_weekly.index = df_weekly.index - pd.DateOffset(days=(df_weekly.index[0] - offset).days)
   
    # Reset the index to keep the first date of each week
    df_weekly.reset_index(inplace=True)
    
    df_weekly.rename(columns={"retail_and_recreation_percent_change_from_baseline": "retail_and_recreation", "grocery_and_pharmacy_percent_change_from_baseline": "grocery_and_pharmacy", "transit_stations_percent_change_from_baseline": "transit_stations"}, inplace=True)
    
    # Filter the dataframe based on the category
    df_final = df_weekly[["date", category]]
    
    return df_final
