API
===

Overview
--------

This document provides a detailed overview of the various functions
implemented across different modules, including their descriptions and
parameter requirements.

File: contact_matrix.py
-----------------------

Function: get_age_group_count_map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Computes the count of different age groups for a
      given city, date range, and consumption distribution.

-  **Parameters**:

   -  df (pd.DataFrame): Input data containing demographic and other
         relevant information.

   -  age_groups (list): List of age group ranges to be analyzed.

   -  consumption_distribution (dict): Distribution of consumption
         across different age groups.

   -  start_date (datetime): Start date for the analysis period.

   -  end_date (datetime): End date for the analysis period.

   -  city (str): Name of the city to filter the data.

   -  epsilon (float, optional): Privacy budget parameter. Default is
         1.0.

Function: get_contact_matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Generates a contact matrix by comparing the sample
      distribution with the overall population distribution.

-  **Parameters**:

   -  sample_distribution (list): Sample distribution of different age
         groups.

   -  population_distribution (list): Population distribution of
         different age groups.

Function: get_pearson_similarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Calculates the Pearson similarity for the given
      contact matrix to determine correlations between different age
      groups.

-  **Parameters**:

   -  contact_matrix (np.array): Matrix representing contact rates
         between different age groups.

File: hotspot_analyzer.py
-------------------------

Function: hotspot_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Analyzes hotspot regions within a city for a given
      date range, considering privacy-preserving mechanisms.

-  **Parameters**:

   -  **df** (pd.DataFrame): Data containing location and movement
         information.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **start_date** (datetime): Start date for the analysis period.

   -  **end_date** (datetime): End date for the analysis period.

   -  **city** (str): Name of the city to perform the analysis on.

   -  **default_city** (str): Default city to use for missing or invalid data.

   -  **epsilon** (float): Privacy budget parameter controlling differential privacy.

-  **Returns**: Processed DataFrame with hotspot predictions.

File: mobility_analyzer.py
--------------------------

Function: mobility_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Analyzes mobility patterns within a city for a
      specified date range while ensuring data privacy.

-  **Parameters**:

   -  **df** (pd.DataFrame): Data containing mobility information.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **start_date** (datetime): Start date for the analysis period.

   -  **end_date** (datetime): End date for the analysis period.

   -  **city** (str): Name of the city to perform the analysis on.

   -  **default_city** (str): Default city to use for missing or invalid data.

   -  **category** (str): Category of mobility to analyze (e.g., "Airlines").

   -  **epsilon** (float): Privacy budget parameter controlling differential privacy.

-  **Returns**: Processed DataFrame with mobility predictions.

File: pandemic_adherence_analyzer.py
------------------------------------

Function: pandemic_adherence_analyzer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Analyzes adherence to pandemic-related guidelines within a city for a specified date range while ensuring data privacy.

-  **Parameters**:

   -  **df** (pd.DataFrame): Data containing transactional information.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **start_date** (datetime): Start date for the analysis period.

   -  **end_date** (datetime): End date for the analysis period.

   -  **city** (str): Name of the city to perform the analysis on.

   -  **default_city** (str): Default city to use for missing or invalid data.

   -  **essential_or_luxury** (str): Category of transactions to analyze (e.g., "Essential" or "Luxury").

   -  **epsilon** (float): Privacy budget parameter controlling differential privacy.

-  **Returns**: Processed DataFrame with adherence analysis results.

File: viz.py
------------

Function: create_hotspot_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Creates a Dash application for visualizing hotspot
      analysis results.

-  **Parameters**:

   -  df (pd.DataFrame): Data used for visualization.

Function: update_graph
~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Updates the hotspot graph based on user inputs.

-  **Parameters**:

   -  start_date (datetime): Start date for filtering data.

   -  end_date (datetime): End date for filtering data.

   -  epsilon (float): Privacy budget parameter.

   -  city (str): City to filter data by.

Function: create_mobility_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Creates a Dash application for visualizing mobility
      analysis results.

-  **Parameters**:

   -  df (pd.DataFrame): Data used for visualization.

.. _function-update_graph-1:

Function: update_graph
~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Updates the mobility graph based on user inputs.

-  **Parameters**:

   -  start_date (datetime): Start date for filtering data.

   -  end_date (datetime): End date for filtering data.

   -  city_filter (str): City to filter data by.

   -  epsilon (float): Privacy budget parameter.

Function: create_pandemic_stage_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Creates a Dash application for visualizing pandemic
      stage analysis results.

-  **Parameters**:

   -  df (pd.DataFrame): Data used for visualization.

.. _function-update_graph-2:

Function: update_graph
~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Updates the pandemic stage graph based on user
      inputs.

-  **Parameters**:

   -  start_date (datetime): Start date for filtering data.

   -  end_date (datetime): End date for filtering data.

   -  city_filter (str): City to filter data by.

   -  essential_or_luxury (str): Category of item consumption to analyze
         ('essential' or 'luxury').

   -  epsilon (float): Privacy budget parameter.

Function: create_contact_matrix_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Creates a Dash application for visualizing the
      contact matrix.

-  **Parameters**:

   -  df (pd.DataFrame): Data used for visualization.

Function: update_contact_matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Updates the contact matrix visualization based on
      user inputs.

-  **Parameters**:

   -  start_date (datetime): Start date for filtering data.

   -  end_date (datetime): End date for filtering data.

   -  city (str): City to filter data by.

   -  epsilon (float): Privacy budget parameter.
