Usage
=====

.. _installation:

Installation
------------

To use DP_epidemiology, first install it using pip:

.. code-block:: console

   (.venv) $ pip install DP_epidemiology

.. _usage:

Usage
----------------

To do hotspot detection.
you can use the ``hotspot_analyzer.hotspot_analyzer`` function:

.. autofunction:: hotspot_analyzer.hotspot_analyzer

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> import DP_epidemiology
>>> hotspot_analyzer.hotspot_analyzer()
['shells', 'gorgonzola', 'parsley']