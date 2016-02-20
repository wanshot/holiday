Requiremants
----------------

- Python 2.7

Install
----------------

.. code-block:: shell

   $ pip install holiday

Usage
----------------


.. code-block:: python

   >>> holiday = Holiday([
   ...     (2016, 1, 1, "fri", 1),
   ...     (2016, 1, 2, "sat", 1),
   ... ])
   >>> holiday.is_holiday(date(2016, 1, 1))
   True
   >>> holiday.is_holiday(date(2016, 1, 3))
   False

- Express all values that can take in the field in asterisk (*)

.. code-block:: python

   >>> holiday = Holiday([
   ...     ("*", 1, 1, "fri", 1),
   ...     ("*", 1, 1, "thu", 1),
   ... ])
   >>> holiday.is_holiday(date(2016, 1, 1))
   True
   >>> holiday.is_holiday(date(2015, 1, 1))
   True
   >>> holiday.is_holiday(date(2014, 1, 1))
   False

- is_business_day() returns the inverse of the truth-value of the is_holiday()

.. code-block:: python

    >>> holiday = Holiday([
    ...     ("*", "*", "*", "*", "*"),
    ... ])
    >>> holiday.is_holiday(date(2000, 1, 1))
    True
    >>> holiday.is_business_day(date(2000, 1, 1))
    False

License
--------

This software is released under the MIT License, see LICENSE.txt.
