Usage
=====

.. _installation:

Installation
------------

To use DP_epidemiology, first install it using pip:

.. code-block:: console

   (.venv) $ pip install DP_epidemiology

.. _usage:

Tools
-----

To do hotspot detection,
you can use the ``hotspot_analyzer.hotspot_analyzer()`` function to generate differential private release of transactional data per zip code:

.. autofunction:: hotspot_analyzer.hotspot_analyzer

The ``df`` parameter take pandas dataframe as input with columns ``[ "ID" "date" "merch_category" "merch_postal_code" "transaction_type" "spendamt"	"nb_transactions"]``.
The ``start_date`` and  ``end_date`` parameters take the start and end date of the time frame for which the analysis is to be done.
The ``city`` parameter takes the name of the city for which the analysis is to be done.
The ``epsilon`` parameter takes the value of epsilon for differential privacy.

For example:

>>> import DP_epidemiology import hotspot_analyzer
>>> from datetime import datetime
>>> df = pd.read_csv('data.csv')
>>> hotspot_analyzer.hotspot_analyzer(df,datetime(2020, 9, 1),datetime(2021, 3, 31),"Medellin",10)
	df_nb_transactions	postal_code
0	182274	500001
1	184207	500002
2	181038	500003
3	178536	500004
4	202206	500005
5	189752	500006
6	205064	500007
7	166509	500008
8	194870	500009
9	188950	500010
10	175238	500011
11	165529	500012
12	190527	500013
13	214845	500014
14	191987	500015
15	192571	500016
16	193769	500017
17	218482	500020
18	205344	500021
19	214316	500022
20	185675	500023
21	212889	500024
22	206160	500025
23	185104	500026
24	202548	500027
25	180732	500028
26	207612	500030
27	207333	500031
28	221113	500032
29	193680	500033
30	176496	500034
31	190031	500035
32	176728	500036
33	163655	500037
34	178762	500040
35	185492	500041
36	188731	500042
37	228704	500043
38	165511	500044
39	182983	500046
40	190199	500047
41	183694	55411

To do visulize the hotspot,
you can use the ``viz.create_hotspot_dash_app()`` function to generate differential private release of transactional data per zip code:

.. autofunction:: viz.create_hotspot_dash_app

The ``df`` parameter take pandas dataframe as input with columns ``[ "ID" "date" "merch_category" "merch_postal_code" "transaction_type" "spendamt"	"nb_transactions"]``.

For example:

>>> import DP_epidemiology import viz
>>> df = pd.read_csv('data.csv')
>>> app=viz.create_hotspot_dash_app(df)
>>> app.run_server(debug=True)

.. image:: images/hotspot.png
   :alt: hotspot


To do mobility inference,
you can use the ``mobility_analyzer.mobility_analyzer()`` function to generate differential private time series of trnsactional data in the "Airlines" category:

.. autofunction:: mobility_analyzer.mobility_analyzer

The ``df`` parameter take pandas dataframe as input with columns ``[ "ID" "date" "merch_category" "merch_postal_code" "transaction_type" "spendamt"	"nb_transactions"]``.
The ``start_date`` and  ``end_date`` parameters take the start and end date of the time frame for which the analysis is to be done.
The ``city`` parameter takes the name of the city for which the analysis is to be done.
The ``epsilon`` parameter takes the value of epsilon for differential privacy.

For example:

>>> import DP_epidemiology import mobility_analyzer
>>> from datetime import datetime
>>> df = pd.read_csv('data.csv')
>>> mobility_analyzer.mobility_analyzer(df,datetime(2020, 9, 1),datetime(2021, 3, 31),"Medellin",10)
   nb_transactions       date
0              1258 2020-09-01
1              1328 2020-09-08
2              1281 2020-09-15
3              1162 2020-09-22
4              1182 2020-09-29
5              1264 2020-10-06
6              1450 2020-10-13
7              1294 2020-10-20
8              1238 2020-10-27
9              1285 2020-11-03
10             1297 2020-11-10
11             1276 2020-11-17
12             1271 2020-11-24
13             1280 2020-12-01
14             1128 2020-12-08
15             1188 2020-12-15
16             1208 2020-12-22
17             1138 2020-12-29
18             1218 2021-01-05
19             1252 2021-01-12
20             1302 2021-01-19
21             1194 2021-01-26
22             1287 2021-02-02
23             1333 2021-02-09
24             1315 2021-02-16
25             1508 2021-02-23
26             1394 2021-03-02
27             1301 2021-03-09
28             1493 2021-03-16
29             1200 2021-03-23
30             1371 2021-03-30

To do pandemic stage inference,
you can use the ``pandemic_stage_analyzer.pandemic_stage_analyzer()`` function to generate differential private time series of trnsactional data for luxurious or essential goods:

.. autofunction:: pandemic_stage_analyzer.pandemic_stage_analyzer

The ``df`` parameter take pandas dataframe as input with columns ``[ "ID" "date" "merch_category" "merch_postal_code" "transaction_type" "spendamt"	"nb_transactions"]``.
The ``start_date`` and  ``end_date`` parameters take the start and end date of the time frame for which the analysis is to be done.
The ``city`` parameter takes the name of the city for which the analysis is to be done.
The``essential_or_luxury`` parameter takes the value of "essential" or "luxury" for which the analysis is to be done.
The ``epsilon`` parameter takes the value of epsilon for differential privacy.

For example:

>>> import DP_epidemiology import pandemic_stage_analyzer
>>> from datetime import datetime
>>> df = pd.read_csv('data.csv')
>>> pandemic_stage_analyzer.pandemic_stage_analyzer(df,start_date,end_date,"Medellin",essential_or_luxury="luxury",epsilon=10)

To get the contact matrix,
you need to first get the age group count map using the ``contact_matrix.get_age_group_count_map()`` function:

.. autofunction:: contact_matrix.get_age_group_count_map

The ``df`` parameter take pandas dataframe as input with columns ``[ "ID" "date" "merch_category" "merch_postal_code" "transaction_type" "spendamt"	"nb_transactions"]``.
The ``start_date`` and  ``end_date`` parameters take the start and end date of the time frame for which the analysis is to be done.
The ``pincode_prefix`` parameter indicating the starting digits that is common to all the pincodes of the country.
The ``epsilon`` parameter takes the value of epsilon for differential privacy.

For example:

>>> import DP_epidemiology import contact_matrix
>>> from datetime import datetime
>>> df = pd.read_csv('data.csv')
>>> contact_matrix.get_age_group_count_map(df,datetime(2020, 12, 12),datetime(2021, 1, 31),pincode_prefix="70",epsilon=1.0)

Then you can use the ``contact_matrix.get_contact_matrix()`` function to generate differential private contact matrix:

.. autofunction:: contact_matrix.get_contact_matrix

The ``age_group_sample_size`` parameter takes the age group sample size distribution list. This will be generated by using the values from the map returned by the ``get_age_group_count_map()`` function.
The ``age_group_population_distribution`` parameter takes the age group population distribution list for the country.

For example:

>>> import DP_epidemiology import contact_matrix
>>> from datetime import datetime
>>> df = pd.read_csv('data.csv')
>>> age_group_count_map = contact_matrix.get_age_group_count_map(df,datetime(2020, 12, 12),datetime(2021, 1, 31),pincode_prefix="70",epsilon=1.0)
>>> contact_matrix.get_contact_matrix(list(age_group_count_map.values()),age_group_population_distribution)

