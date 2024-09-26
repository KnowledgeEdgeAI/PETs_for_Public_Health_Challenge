# Hotspot Detection, Mobility, and Pandemic Stages using Differential Privacy

## 1. Hotspot Detection

### Assumptions
- **Transaction type**: Only "OFFLINE" transactions contribute to physical hotspots.
- **Transaction metric**: Number of transactions is more relevant than the total value of transactions.
- **Maximum transaction cap**: Maximum number of transactions (`nb_transaction`) is assumed to be 454. Setting a bound of `(0,600)`.
- **Public data**: Number of postal codes in a city is assumed to be public information.

### Algorithm
1. **Add City Column**: A new `city` column is added based on the postal codes (`make_preprocess_location`).
2. **Filter OFFLINE Transactions**: Only "OFFLINE" transactions are considered (`make_filter`).
3. **Filter City Postal Codes**: Filter for the postal codes of the selected city (`make_filter`).
4. **Filter by Time Frame**: Filter data for the selected time frame (`make_truncate_time`).
5. **Transaction Summing & Noise Addition**: Sum the number of transactions by postal code, and add Gaussian noise (`make_private_sum_by`).
6. **Visualization**: Differentially private data is plotted on a colored map for hotspot visualization.

### Sensitivity and Epsilon Analysis
- **Sensitivity per Zip Code**: Sensitivity is 3 for each zip code (due to up to 3 postal codes for each merchant).
- **Scaling with Time**: For multiple time stamps, sensitivity is `3 * no_of_time_stamps`.
- **Epsilon Budget**: The epsilon spent per zip code is `∈ / total_number_of_zip_codes`.
- **Scale Calculation**: `Scale = (3 * no_of_time_stamps * no_of_zip_codes) / ∈`.

---

## 2. Mobility Detection (Airline Merch Category)

### Description
This analysis tracks mobility by monitoring transactions in the "Airlines" category, which reflects the transportation sector.

### Assumptions
- **Transaction metric**: Number of transactions is more relevant than the total value.
- **Online and Offline transactions**: Both contribute to mobility inference.
- **Maximum transaction cap**: Maximum number of transactions (`nb_transaction`) is assumed to be 454. Setting a bound of `(0,600)`.

### Algorithm
1. **Add City Column**: A new `city` column is added based on postal codes (`make_preprocess_location`).
2. **Filter for City**: Data for the selected city is filtered (`make_filter`).
3. **Filter for Airline Category**: Only transactions in the "Airline" category are considered (`make_filter`).
4. **Filter by Time Frame**: Data is filtered for the selected time frame (`make_truncate_time`).
5. **Transaction Summing & Noise Addition**: Sum the number of transactions by postal code for each timestep and add Gaussian noise (`make_private_sum_by`).

### Sensitivity and Epsilon Analysis
- **Sensitivity per Merchant**: Sensitivity is 3 for each merchant in the "Airline" category.
- **Scaling with Time**: For multiple timesteps, sensitivity is `3 * no_of_time_steps`.
- **Epsilon Budget**: The epsilon spent per timestep is `∈ / no_of_timesteps`.
- **Scale Calculation**: `Scale = (3 * no_of_time_steps * no_of_time_steps) / ∈`.

### Validation
- **External Data Comparison**: Compare mobility results with publicly available COVID-19 mobility reports (e.g., [Google COVID-19 Mobility Report for Bogotá](https://www.gstatic.com/covid19/mobility/2022-10-15_CO_Bogota_Mobility_Report_en.pdf)).

---

## 3. Pandemic Stages Detection

### Description
Analyzes transaction behavior to identify pandemic stages by comparing transactions in essential vs luxurious goods categories.

### Assumptions
- **Essential Goods**: Includes Utilities (Electric, Gas, Water), Drug Stores, Grocery Stores, Hospitals, General Retail Stores.
- **Luxurious Goods**: Includes Hotels, Bars, Restaurants.
- **Transaction metric**: Number of transactions is more relevant than the total value.
- **Online and Offline transactions**: Both are considered.

### Algorithm
1. **Add City Column**: A new `city` column is added based on postal codes (`make_preprocess_location`).
2. **Filter for City**: Data for the selected city is filtered (`make_filter`).
3. **Add Super Category Column**: A new `merch_super_category` column is added for classifying transactions into luxurious and essential categories (`make_preprocess_location`).
4. **Filter by Super Category**: Only transactions related to luxurious goods are filtered out (`make_filter`).
5. **Filter by Time Frame**: Data is filtered for the selected time frame (`make_truncate_time`).
6. **Transaction Summing & Noise Addition**: Sum the number of transactions by postal code and add Gaussian noise (`make_private_sum_by`).
7. **Visualization**: Differentially private data is plotted for visualization of pandemic stages.

### Sensitivity and Epsilon Analysis
- **Sensitivity per Category**: Sensitivity is 3 for each category (essential or luxurious goods).
- **Scaling with Time**: For multiple timesteps, sensitivity is `3 * no_of_time_steps`.
- **Epsilon Budget**: The epsilon spent per timestep is `∈ / no_of_timesteps`.
- **Scale Calculation**: `Scale = (3 * no_of_time_steps * no_of_time_steps) / ∈`.

---

## 4. Contact Pattern Matrix Estimation

### Description
Estimates the contact matrix by analyzing transactional data for different age groups across various merchandise categories.

### Assumptions
- **Proportion of Age Groups**: Assumed participation in merchandise categories follows an age group proportion map:
  ```python
  age_group_proportion_map = {
      'Airlines': [25, 40, 35],
      'Bars/Discotheques': [50, 35, 15],
      'Hospitals': [15, 40, 45],
      'Drug Stores': [15, 40, 45],
      'Computer Network': [40, 35, 25],
      'General Retail Stores': [20, 50, 30],
      'Grocery Stores': [20, 50, 30],
      'Utilities': [10, 40, 50],
      'Hotels': [30, 40, 30],
      'Restaurants': [35, 40, 25]
  }
  
### Algorithm

1. **Filter Week**: Select the specific week for analysis.
2. **Filter City**: Choose the city of interest (e.g., Bogotá).
3. **Filter OFFLINE Transactions**: Only consider offline transactions.
4. **Group by Merchant Category**: Sum the number of transactions (`nb_transactions`).
5. **Private Count of Postal Codes**: Obtain the private count of unique postal codes for each merchant category and week.
6. **Compute Private Mean Transactions**: Calculate the average number of transactions per zip code using the age group proportion map.

### Challenges

- Ensuring the contact matrix accurately reflects transaction participation from different age groups.
- Making the contact matrix symmetric to ensure mutual interaction between age groups.
- Difficulty in gathering granular public data for more detailed age group division.
