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
['shells', 'gorgonzola', 'parsley']