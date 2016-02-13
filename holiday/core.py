# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import date as _date
from collections import defaultdict

from .exceptions import (
    ParseError,
    PeriodRangeError
)
from .parser import ParseDate


WEEK_MAP = {
    "mon": 1,
    "tue": 2,
    "wed": 3,
    "thu": 4,
    "fri": 5,
    "sat": 6,
    "sun": (7, 0),
}

SAT = ('*', '*', '*', 'sat', '*')
SUN = ('*', '*', '*', 'sun', '*')

TIME_RANGES = {
    'years': (1, 9999),
    'months': (1, 12),
    'days': (1, 31),
    'weeks': (1, 7),
    'number_weeks': (1, 5),
}


class Holiday(object):
    """
    Base class
    """

    def __init__(self, times):
        """
        :param tuple of list times: plz see below
        """
        # ('*', '*', '*', '*', '*')
        #   ┬   ┬   ┬   ┬   ┬
        #   │   │   │   │   │
        #   │   │   │   │   │
        #   │   │   │   │   └─  number of week (1 - 5)
        #   │   │   │   └─── day of week (1 to 7 are Sunday to Saturday)
        #   │   │   └───── day of month (1 - 31)
        #   │   └─────── month (1 - 12)
        #   └───────── year (1 - 9999)

        self._check_arg(times)

        self.years = defaultdict(set)
        self.months = defaultdict(set)
        self.days = defaultdict(set)
        self.day_of_weeks = defaultdict(set)
        self.num_of_weeks = defaultdict(set)

        func = lambda d, key, value: d[key].add(value)

        for idx, (year, month, day, day_of_week, num_of_week) in enumerate(times):
            func(self.years, year, idx)
            func(self.months, month, idx)
            func(self.days, day, idx)
            if isinstance(day_of_week, str):
                day_of_week = WEEK_MAP[day_of_week]
            func(self.day_of_weeks, day_of_week, idx)
            func(self.num_of_weeks, num_of_week, idx)

    def _check_arg(self, times):

        if not isinstance(times, list):
            raise TypeError("an list is required")

        for time in times:

            if not isinstance(time, tuple):
                raise TypeError("an tuple is required")

            if len(time) > 5:
                raise TypeError("Target time takes at most 5 arguments"
                                " ('%d' given)" % len(time))

            if len(time) < 5:
                time_labels_order = ("year", "month", "day", "day of week", "number of week")
                raise TypeError("Required argument '%s' (pos '%d')"
                                " not found" % (time_labels_order[len(time)], len(time)))

    def _check_int_time_format(self, time_name, values):
        """ check time

        :param time name of String time_name: years or months or days or number week
        :param List of times values: Number or the asterisk in the list
        :rtype: list
        :raises PeriodRangeError: outside the scope of the period
        :return: It returns a value if there is no exception
        """

        start, end = TIME_RANGES[time_name]

        for value in values:

            if not isinstance(value, int):
                raise TypeError("'%s' is not an int" % value)

            if value not in range(start, end):
                raise PeriodRangeError("'%d' is outside the scope of the period "
                                       "'%s' range: '%d' to '%d'" % (
                                           value, time_name, start, end
                                       ))

        return values

    def _check_weeks_string(self, values):
        """ check weeks

        :param List of weeks values: List of day of the week
        :rtype: list
        :raises ParseError: When the value can not be parsed
        :return: It returns a value if there is no exception
        """

        exclude_weeks = set()
        checked_weeks = [v if v in WEEK_MAP else exclude_weeks.add(v) for v in values]

        if not exclude_weeks:
            return checked_weeks

        raise ParseError("The value could not be perse")

    def is_holiday(self, date, cron=None):
        """ whether holiday
        """

        result = []
        week_num = date.isoweekday()
