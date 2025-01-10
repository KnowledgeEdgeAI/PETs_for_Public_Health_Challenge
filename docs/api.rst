API
===

Overview
--------

This document provides a detailed overview of the various functions
implemented across different modules, including their descriptions and
parameter requirements.

File: contact_matrix.py
-----------------------

Function: validate_input_data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Validates the input data for city, date range, and
      consumption categories, ensuring consistency and completeness.

-  **Parameters**:

   -  **df** (pd.DataFrame): Data containing transaction and location
         information.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **age_groups** (list): List of age group ranges to validate.

   -  **consumption_distribution** (dict): Expected distribution of consumption across different categories.

   -  **start_date** (datetime): Start date for the analysis period.

   -  **end_date** (datetime): End date for the analysis period.

   -  **city** (str): Name of the city to validate.

   -  **default_city** (str): Default city to use for missing or invalid data.

Function: get_private_counts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Computes differentially private counts of transactions
      across categories for a specified city and time period.

-  **Parameters**:

   -  **df** (pd.DataFrame): Data containing transaction information.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **categories** (list): List of categories to calculate counts for.

   -  **start_date** (datetime): Start date for the analysis period.

   -  **end_date** (datetime): End date for the analysis period.

   -  **city** (str): Name of the city to filter the data.

   -  **default_city** (str): Default city to use for missing or invalid data.

   -  **epsilon** (float, optional): Privacy budget parameter. Default is 1.0.

Function: get_age_group_count_map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Computes the count of different age groups for a
      given city, date range, and consumption distribution.

-  **Parameters**:

   -  **df** (pd.DataFrame): Input data containing demographic and other
         relevant information.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **age_groups** (list): List of age group ranges to be analyzed.

   -  **consumption_distribution** (dict): Distribution of consumption
         across different age groups.

   -  **start_date** (datetime): Start date for the analysis period.

   -  **end_date** (datetime): End date for the analysis period.

   -  **city** (str): Name of the city to filter the data.

   -  **default_city** (str): Default city to use for missing or invalid data.

   -  **epsilon** (float, optional): Privacy budget parameter. Default is 1.0.

Function: get_contact_matrix_country
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Computes the average contact matrix for a group of
      cities based on population distribution and scaling factors.

-  **Parameters**:

   -  **counts_per_city** (list): List of age group counts for each city.

   -  **population_distribution** (list): Overall population distribution
         across age groups.

   -  **scaling_factor** (float): Scaling factor to adjust contact rates.

Function: get_contact_matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Generates a contact matrix by comparing the sample
      distribution with the overall population distribution.

-  **Parameters**:

   -  **sample_distribution** (list): Sample distribution of different age
         groups.

   -  **population_distribution** (list): Population distribution of
         different age groups.

Function: plot_difference
~~~~~~~~~~~~~~~~~~~~~~~~~

-  **Description**: Visualizes the difference between two contact matrices.

-  **Parameters**:

   -  **A** (np.array): First contact matrix.

   -  **B** (np.array): Second contact matrix.

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
      analysis results, including an interactive graph updated based on user inputs.

-  **Parameters**:

   -  **df** (pd.DataFrame): Data used for visualization.

   -  **city_zipcode_map** (pd.DataFrame): Mapping between cities and their corresponding zip codes.

   -  **default_city** (str): Default city to use for missing or invalid data.

-  **Internal Callback Updates**:

   -  The `update_graph` callback is defined within the function to dynamically update the graph based on the following user inputs:
      
      -  **start_date** (datetime): Start date for filtering data.
      
      -  **end_date** (datetime): End date for filtering data.
      
      -  **epsilon** (float): Privacy budget parameter.
      
      -  **city** (str): City to filter data by.
      
   -  The callback:
      
      1. Filters data using the `hotspot_analyzer` function.
      
      2. Retrieves geographical coordinates for the filtered data using `get_coordinates`.
      
      3. Visualizes transaction locations with a Plotly Express scatter_geo plot, customized with city-centered maps and transaction-based color scaling.

Function: create_mobility_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Description**: Creates a Dash application for visualizing mobility analysis results.

- **Parameters**:

  - df (pd.DataFrame): Data used for visualization.
  - city_zipcode_map (pd.DataFrame): Mapping between cities and zip codes (optional).
  - default_city (str): Default city to display if not selected (optional).

**Layout**:

The function defines the layout of the Dash app using HTML elements for various components:

  - `dcc.DatePickerSingle`: Two date pickers for selecting start and end dates.
  - `dcc.Slider`: Slider for setting the privacy budget parameter (epsilon).
  - `dcc.Dropdown`: Dropdown menus for selecting city and category.
  - `dcc.Graph`: Placeholder for the mobility graph.

**Callback (update_graph)**:

The `update_graph` function is defined within `create_mobility_dash_app` as a callback function using `@app.callback`. It updates the `'mobility-graph'` figure based on user input from the various components.

  - It retrieves user-selected start date, end date, city filter, category, and epsilon value.
  - Converts date strings to datetime objects.
  - Calls the `mobility_analyzer` function (assumed to be defined elsewhere) to filter and analyze data.
  - Creates a line chart using Plotly Express with appropriate labels and title.
  - For the city "Bogota", it adds shapes and annotations for specific events.
  - Finally, the function returns the updated figure.

Function: create_pandemic_stage_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Description**: Creates a Dash application for visualizing pandemic adherence analysis results. Users can explore trends in essential and luxury entries across different cities and dates while adjusting the privacy budget parameter (epsilon).

**Parameters**:

  - `df` (pd.DataFrame): Dataframe containing transaction information.
  - `city_zipcode_map` (pd.DataFrame): Mapping between cities and their corresponding zip codes (optional).
  - `default_city` (str): Default city to use for missing or invalid data (optional).

**Layout**:

  - The application layout uses HTML components to create a user interface:
      - Two `dcc.DatePickerSingle` components allow users to select a start and end date for analysis.
      - A `dcc.Slider` component enables adjusting the privacy budget parameter (epsilon).
      - Dropdown menus (`dcc.Dropdown`) are provided for selecting a city and entry type (essential or luxury).
      - A `dcc.Graph` component displays the resulting line chart.

**Callback (update_graph)**:

  - The `update_graph` function is defined as a callback within `create_pandemic_adherence_dash_app` using `@app.callback`. It dynamically updates the graph based on user input:
      - It retrieves user-selected start date, end date, city filter, entry type (essential or luxury), and epsilon value.
      - Converts date strings to datetime objects.
      - Calls the `pandemic_adherence_analyzer` function (assumed to be defined elsewhere) to filter and analyze data based on the provided parameters.
      - Creates a line chart using Plotly Express with appropriate labels and title, visualizing the number of transactions over time.
      - For the city "Bogotá", it adds shapes and annotations to highlight specific events that might have influenced pandemic adherence.
      - Finally, the function returns the updated figure for the graph.

Function: create_contact_matrix_dash_app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Description**: Creates a Dash application for visualizing contact matrices, showing the interaction rates between different age groups. The application allows users to filter by date and city, and adjust a privacy parameter (epsilon) that may affect underlying calculations (though not directly shown in this code).

**Parameters**:

  - `df` (pd.DataFrame): Dataframe containing location and potentially demographic information used for calculating contact rates.
  - `city_zipcode_map` (pd.DataFrame): Mapping between cities and their corresponding zip codes. Used for filtering data by city.
  - `default_city` (str): Default city to use for missing or invalid data.
  - `age_groups` (list, optional): List of age group labels (e.g., ['0-4', '5-9', ...]). Defaults to a predefined list if not provided.
  - `consumption_distribution` (pd.DataFrame, optional): Distribution of consumption across categories. Used in the `get_age_group_count_map` function. Defaults to reading from "consumption_distribution.csv".
  - `P` (numpy.ndarray, optional): Population distribution across age groups. Defaults to a hardcoded array if not provided.
  - `scaling_factor` (numpy.ndarray or similar, optional): Scaling factors used in contact matrix calculation. Defaults to reading from "fractions_offline.csv".

**Layout**:

  - The application layout uses HTML components to create a user interface:
      - Two `dcc.DatePickerSingle` components allow users to select a start and end date for analysis.
      - A `dcc.Slider` component enables adjusting the privacy budget parameter (epsilon). This parameter is passed to the callback but its direct effect on the visualized matrix is not shown in this code. It likely affects the data processing in `get_age_group_count_map`.
      - A `dcc.Dropdown` component allows users to select a city.
      - A `dcc.Graph` component displays the resulting heatmap of the contact matrix.
      - A `html.Div` component displays the raw contact matrix values in a readable format.

**Callback (update_contact_matrix)**:

  - The `update_contact_matrix` function is defined as a callback within `create_contact_matrix_dash_app` using `@app.callback`. It dynamically updates the heatmap and matrix output based on user input:
      - It retrieves user-selected start date, end date, city, and epsilon value.
      - Converts date strings to datetime objects.
      - Calls the `get_age_group_count_map` function to get age group counts for the selected city and date range. This function also uses the `city_zipcode_map`, `age_groups`, `consumption_distribution`, and `default_city` parameters.
      - Uses a hardcoded `age_group_population_distribution` (`P`) and a `scaling_factor` (read from a file by default) to generate the contact matrix using `get_contact_matrix_country`.
      - Creates a heatmap of the contact matrix using Plotly Express `px.imshow`, with appropriate labels and a 'viridis' color scale.
      - Formats the contact matrix as a string for display in the output div.
      - Returns both the figure for the heatmap and the formatted matrix string.

**Data Preprocessing and Defaults**:

  - The function preprocesses the input dataframe `df` using `make_preprocess_location()`.
  - It handles default values for `age_groups`, `consumption_distribution`, `P`, and `scaling_factor` if they are not provided by the user.
