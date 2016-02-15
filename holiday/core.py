# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import (
    defaultdict,
    OrderedDict,
)
from datetime import date as _date
from itertools import product

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

ORDER_WEEK = OrderedDict({v: k for k, v in WEEK_MAP.items()})

_time_data = (
    ("year", (1, 9999)),
    ("month", (1, 12)),
    ("day", (1, 31)),
    ("day_of_week", (1, 7)),
    ("num_of_week", (1, 6)),
)

TIME_INFO = OrderedDict()
TIME_INFO.update(OrderedDict(_time_data))
TIME_LABEL = TIME_INFO.keys()


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

        self._check_times(times)

        self.year = defaultdict(set)
        self.month = defaultdict(set)
        self.day = defaultdict(set)
        self.day_of_week = defaultdict(set)
        self.num_of_week = defaultdict(set)

        func = lambda d, key, value: d[key].add(value)

        for idx, (year, month, day, day_of_week, num_of_week) in enumerate(times):
            func(self.year, year, idx)
            func(self.month, month, idx)
            func(self.day, day, idx)
            func(self.day_of_week, day_of_week, idx)
            func(self.num_of_week, num_of_week, idx)

    def _check_times(self, times):
        """
        """

        if not isinstance(times, list):
            raise TypeError("an list is required")

        for time in times:

            if not isinstance(time, tuple):
                raise TypeError("an tuple is required")

            if len(time) > 5:
                raise TypeError("Target time takes at most 5 arguments"
                                " ('%d' given)" % len(time))

            if len(time) < 5:
                raise TypeError("Required argument '%s' (pos '%d')"
                                " not found" % (TIME_LABEL[len(time)], len(time)))

            self._check_int_time_format(TIME_LABEL, time)

    def _check_int_time_format(self, labels, values):
        """ check time

        :param time name of String time_name: years or months or days or number week
        :param List of times values: Number or the asterisk in the list
        :rtype: list
        :raises PeriodRangeError: outside the scope of the period
        :return: It returns a value if there is no exception
        """

        for label, value in zip(labels, values):

            if value == "*":
                continue

            if label == "day_of_week":
                if isinstance(value, (str, unicode)):
                    if value not in WEEK_MAP.keys():
                        raise TypeError("'%s' is not day of the week. "
                                        "character is the only '%s'" % (
                                            value, ', '.join(ORDER_WEEK.values())
                                        ))

            if label in ["year", "month", "day", "num_of_week"]:

                if not isinstance(value, int):
                    raise TypeError("'%s' is not an int" % value)

                start, end = TIME_INFO[label]

                if not start <= value <= end:
                    raise PeriodRangeError("'%d' is outside the scope of the period "
                                           "'%s' range: '%d' to '%d'" % (
                                               value, label, start, end
                                           ))

    def _convert_holiday_format(self, times):
        """
        """
        result = []

        for year, month, day, day_of_week, num_of_week in times:

            if isinstance(day_of_week, (str, unicode)):
                day_of_week = WEEK_MAP.get(day_of_week, "*")

            result.append((year, month, day, day_of_week, num_of_week))

        return result

    def is_holiday(self, date, cron=None):
        """
        """
        time = [
            date.year,
            date.month,
            date.day,
            date.isoweekday(),
            _extract_week_number(date)
        ]

        target = []
        for key, date in list(zip(TIME_LABEL, time)):
            d = getattr(self, key)
            asterisk = d.get("*", set())
            s = asterisk.union(d.get(date, set()))
            target.append(list(s))

        for result in map(set, product(*target)):
            if len(result) == 1:
                return True
        return False

    def is_business_day(self):
        """
        """
        return not(self.is_holiday)


def _extract_week_number(date):
    first_date = date.replace(day=1)
    return int(date.strftime('%W')) - int(first_date.strftime('%W')) + 1
