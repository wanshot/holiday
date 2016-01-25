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
    "sun": 7,
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
        # ('*', '*', '*', '*', '*')
        #   ┬   ┬   ┬   ┬   ┬
        #   │   │   │   │   │
        #   │   │   │   │   │
        #   │   │   │   │   └─  number of week (1 - 5)
        #   │   │   │   └─── day of week (1 to 7 are Sunday to Saturday)
        #   │   │   └───── day of month (1 - 31)
        #   │   └─────── month (1 - 12)
        #   └───────── year (1 - 9999)
        """

        valid_data = self._clean_holiday_arg(times)

        self.years,
        self.months,
        self.days,
        self.weeks,
        self.number_weeks

        for idx, year, month, day, week, number_week in enumerate(valid_data):


    def _clean_holiday_arg(times):

        if not isinstance(times, list):
            raise TypeError("an list is required")

        for time in times:
            if not isinstance(time, tuple):
                raise TypeError("an tuple is required")
            if len(time) > 5:
                raise TypeError("Target time takes at most 5 arguments"
                                " ('%d' given)" % len(time))
            if len(time) < 5:
                tuple_labels = ("year", "month", "day", "day of week", "number of week")
                raise TypeError("Required argument '%s' (pos '%d')"
                                " not found" % (tuple_labels[len(time)], len(time)))

        return time

    def _create_data_structure(self):
        """ create_data_structure

        :return: return dict of time name keys and period values
        :rtype: dict
        :Example: >>> {"years": [2000, 2001], "months": set([11,12]), ...}
        """

        time_data = {}

        for time_name, (start, end) in TIME_RANGES.items():

            if '*' in self.__dict__[time_name]:
                time_data[time_name] = range(v['start'], v['end']+1)

            elif time_name == 'weeks':
                checked_weeks = self._check_weeks_string(self.__dict__[time_name])
                week_nums = [WEEK_MAP[week] for week in checked_weeks]
                time_data[time_name] = week_nums

            else:
                period = self._check_int_time_format(
                    time_name,
                    set(self.__dict__[time_name])
                )
                time_data[time_name] = period

        return time_data

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

    def is_holiday(self, date=_date.today()):
        """ whether holiday

        :param date_object: Example >>>date(2000, 1, 1)
        :return: return the result of boolean
        :rtype: boolean
        """

        parsed_date = ParseDate(date).as_dict()
        data = self._create_data_structure()

        if len([v for k, v in parsed_date.items() if v in data[k]]) == 5:
            return True

        return False
