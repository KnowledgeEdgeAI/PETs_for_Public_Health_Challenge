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
you can use the ``hotspot_analyzer.hotspot_analyzer()`` function:

.. autofunction:: hotspot_analyzer.hotspot_analyzer

The ``df`` parameter take pandas dataframe as input with columns ``[ "ID" "date" "merch_category" "merch_postal_code" "transaction_type" "spendamt"	"nb_transactions"]``.
The ``start_date`` and  ``end_date`` parameters take the start and end date of the time frame for which the analysis is to be done.
The ``city_filter`` parameter takes the name of the city for which the analysis is to be done.
The ``nb_postal_codes`` parameter takes the number of postal codes in the city.
The ``epsilon`` parameter takes the value of epsilon for differential privacy.

For example:

>>> import DP_epidemiology import hotspot_analyzer
>>> from datetime import datetime
>>> df = pd.read_csv('data.csv')
>>> hotspot_analyzer.hotspot_analyzer(df,datetime(2020, 9, 1),datetime(2021, 3, 31),"Medellin",42,10)
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