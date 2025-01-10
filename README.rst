Differentially private tools of epidemiology for Public Health Challenge by Data.org
===========================================================================================

.. image:: https://readthedocs.org/projects/pets-for-public-health-challenge/badge/?version=latest
    :target: https://pets-for-public-health-challenge.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. This README.rst should render properly both on GitHub and in Sphinx.

Hotspot Analyzer
-----------------

Description

Areas with high physical economic activities can be identified as a pandemic hotspot. This analysis tracks pandemic hotspots by monitoring differential private release of financial transactions in a city and identifying areas with high transaction activity.

Assumptions

* Transaction type : Only ``OFFLINE`` transactions contribute to physical hotspots.  
* Transaction metric : Number of transactions is more relevant than the total value of transactions.  
* Maximum transaction cap : Maximum number of transactions (``nb_transaction``) is assumed to be ``454``. Setting a bound of ``(0,600)``.  
* Public data : Number of postal codes in a city is assumed to be public information.  

Algorithm

#. Add City Column: A new ``city`` column is added based on the postal codes (``make_preprocess_location``).
#. Filter OFFLINE Transactions: Only "OFFLINE" transactions are considered (``make_filter``).
#. Filter City Postal Codes: Filter for the postal codes of the selected city (``make_filter``).
#. Filter by Time Frame : Filter data for the selected time frame (``make_truncate_time``).
#. Transaction Summing & Noise Addition: Sum the number of transactions by postal code, and add Gaussian noise (``make_private_sum_by``).
#. Visualization: Differentially private data is plotted on a colored map for hotspot visualization.

Sensitivity and Epsilon Analysis

* Sensitivity : In a single time stamp, ``1`` merchant can come only once in a particular zip code but can appear in upto ``3`` zip codes. So, if we wanted to release measures about a single zip code sensitivity would be ``1``  but since we want to release data for all zip codes, the sensitivity used for each zip code is ``3``.
* Scaling with Time: For multiple time stamps, sensitivity is ``3 * no_of_time_stamps``.
* Epsilon Budget: The epsilon spent for each query is ``∈``.
* Scale Calculation: ``Scale = (3 * no_of_time_stamps* upper_bound) / ∈``.


Mobility Analyzer
------------------

Description

This analysis tracks mobility by monitoring differential private time series release of financial transactions in the ``retail_and_recreation``, ``grocery_and_pharmacy`` and ``transit_stations`` super categories which matches with google mobility data for easy validation.

Assumptions

* Transaction metric : Number of transactions is more relevant than the total value.
* Online and Offline transactions : Both contribute to mobility inference.
* Maximum transaction cap: Maximum number of transactions (``nb_transaction``) is assumed to be ``454``. Setting a bound of ``(0,600)``.

Algorithm

#. Add City Column: A new ``city`` column is added based on postal codes (``make_preprocess_location``).
#. Add Super Category Column : A new ``merch_super_category`` column is added for classifying transactions into retail_and_recreation, grocery_and_pharmacy and transit_stations categories (``make_preprocess_merchant_mobility``).
#. Filter for City: Data for the selected city is filtered (``make_filter``).
#. Filter for super category: data is filtered for retail_and_recreation, grocery_and_pharmacy and transit_stations categories (``make_filter``).
#. Filter by Time Frame: Data is filtered for the selected time frame (``make_truncate_time``).
#. Transaction Summing & Noise Addition: Sum the number of transactions by postal code for each timestep and add Gaussian noise (``make_private_sum_by``).

Sensitivity and Epsilon Analysis

* Sensitivity per Merchant: Sensitivity is 3 for each merchant.
* Scaling with Time: For multiple timesteps, sensitivity is ``3 * no_of_time_steps``.
* Epsilon Budget: The epsilon spent per timestep is ∈ .
* Scale Calculation: ``Scale = (3 * no_of_time_steps* upper_bound) / ∈``.

Validation

* External Data Comparison: Compare mobility results with publicly available COVID-19 mobility reports, e.g.,  `Google COVID-19 Mobility Report for Bogotá <https://www.gstatic.com/covid19/mobility/2022-10-15_CO_Bogota_Mobility_Report_en.pdf>`_


Pandemic Adherence Analyzer
----------------------------

Description

Analyzes transaction behavior to identify pandemic stages by comparing transactions in essential vs luxurious goods categories.

Assumptions

*  Essential Goods: Includes ``Utilities (Electric, Gas, Water), Drug Stores, Grocery Stores, Hospitals, General Retail Stores``.
*  Luxurious Goods: Includes ``Hotels, Bars, Restaurants``.
*  Transaction metric: Number of transactions is more relevant than the total value.
*  Online and Offline transactions: Both are considered.

Algorithm

#. Add City Column : A new ``city`` column is added based on postal codes (``make_preprocess_location``).
#. Filter for City : Data for the selected city is filtered (``make_filter``).
#. Add Super Category Column : A new ``merch_super_category`` column is added for classifying transactions into luxurious and essential categories (``make_preprocess_location``).
#. Filter by Super Category : Only transactions related to luxurious or essential goods are filtered out (``make_filter``).
#. Filter by Time Frame : Data is filtered for the selected time frame (``make_truncate_time``).
#. Transaction Summing & Noise Addition: Sum the number of transactions by postal code and add Gaussian noise (``make_private_sum_by``).
#. Visualization : Differentially private data is plotted for visualization of pandemic stages.

Sensitivity and Epsilon Analysis

* Sensitivity per Category : Sensitivity is ``3`` for each category (essential or luxurious goods).
* Scaling with Time : For multiple timesteps, sensitivity is ``3 * no_of_time_steps``.
* Epsilon Budget : The epsilon spent per timestep is ∈.
* Scale Calculation : ``Scale = (3 * no_of_time_steps* upper_bound) / ∈``.



Contact Pattern Matrix Estimation
---------------------------------

Description

Estimates the contact matrix by analyzing transactional activities from different age groups.

Assumptions

#. There is a mixing factor for each age group, used to scale its population size when calculating the total number of contacts it makes with people from other age groups.
#. The persons, involved in the transactions, only make contact with individuals also involved in the transactions from the data.
#. Every transaction under ``nb_transactions`` is done by a unique individual and this is true across different merchant IDs as well. Thus, total number of unique individuals is equal to the total number of transactions across all the merchant IDs.
#. The contacts among various age groups is exclusive i.e., every individual, from any given age group, make contact with distinct individuals from other age groups.. In the video, they also took this assumptions.

Algorithm
*Computing the contact patterns across the whole country.*

#. First, calculate the private counts of the total number of transactions for each city in the dataset.  
#. Using these city-level transaction counts, calculate the private counts of the total number of transactions for each age group.  
   For this, the age-group-wise merchandise consumption distribution, referred to as D, is required.  

   *We use a machine learning approach to estimate the age-group-wise merchandise consumption distribution, D, as described below:*  
   *The process begins with an initial estimate of D. Using this estimate, a contact matrix is calculated through the algorithm being described.*  
   *Next, a loss function is chosen to quantify the difference between the ground truth contact matrix and the estimated contact matrix.*  
   *This loss function is iteratively minimized by updating the values in D.*  
   *However, a limitation of this approach is the need to learn D separately for each country, assuming the ground truth contact matrix is available and aligns with the timeframe of the transaction data.*  

#. Calculate the count of contacts between each pair of age groups for each city, and then average these counts across all cities to derive the contact matrix.  
#. Finally, to introduce symmetry in the contact matrix and account for different mixing factors across age groups, multiply the contact matrix by the mixing factor vector and then average it with its transpose.  
   *The mixing factor is estimated using the same approach as for the age-group-wise merchandise consumption distribution, D.*


Sensitivity and Epsilon Analysis

* Sensitivity per Merchant: Sensitivity is 3 for each merchant in the ``Airline`` category.
* Scaling with Time: For multiple timesteps, sensitivity is ``3 * no_of_time_steps``.
* Scaling with Upper Bound: Sensitivity is further scaled by the upper bound of the number of transactions for any merchant category after doing group by with zip code and merchant category. Updated sensitivity is ``3 * no_of_time_steps * upper_bound``.
* Epsilon Budget: The epsilon spent per timestep is ∈ .
* Scale Calculation: ``Scale = (3 * no_of_time_steps * uppper_bound) / ∈``.

Methods of Evaluating Contact Matrix

* Displaying a heatmap of the absolute differences between the ground truth contact matrix and the estimated contact matrix provides a clear visual representation of discrepancies. This helps identify which age group segments show the greatest deviations and in which direction. These insights are valuable for refining the model around specific age groups with larger differences, thereby improving accuracy. Additionally, this method can be extended to track shifts in the contact matrix over time, revealing cross-age group interactions that have increased, decreased, or remained stable. Such trends are instrumental in informing targeted policies.
* Calculating the aggregate sum of the absolute differences between corresponding elements of the ground truth and estimated contact matrices quantifies the overall discrepancy. This metric offers an intuitive understanding of the total divergence between the two matrices in absolute numerical terms, serving as a straightforward and effective measure for model evaluation.

Challenges

* Ensuring the contact matrix accurately reflects transaction participation from different age groups.
* Making the contact matrix symmetric to ensure mutual interaction between age groups.
* Difficulty in gathering granular public data for more detailed age group division.




File Strurcture
---------------
* dist
    * dp_epidemiology-0.0.2-py3-none-any.whl
    * dp_epidemiology-0.0.2.tar.gz

* docs
    * api.rst
    * conf.py
    * index.rst
    * make.bat
    * Makefile
    * requirements.in 
    * requirements.txt - This file contains the required libraries for the project.
    * usage.rst - This file contains the usage of the project.

* src
    * DP_epidemiology
        * contact_matrix.py - This module contains the implementation of the contact matrix estimation.
        * hotspot_analyzer.py - This module contains the implementation of the hotspot detection.
        * mobility_analyzer.py - This module contains the implementation of the mobility detection.
        * pandemic_stage_analyzer.py - This module contains the implementation of the pandemic stage detection.
        * utilities.py - This module contains the utility functions used in the other modules.
        * viz.py - This module contains the function for plotly visualization app for hotspot, mobility, pandemic stage detection and contact matrix estimation.
        * ``__init__.py``

* tests
    * test.py - This module contains the test cases for all the modules in the src folder.
