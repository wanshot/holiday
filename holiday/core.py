# -*- coding: utf-8 -*-
import re
from .exceptions import ParseError, PeriodRangeError
# from .parser import DateParser


MONTH_MAP = {
    1: "jan",
    2: "feb",
    3: "mar",
    4: "apr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "aug",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dec",
}

WEEK_MAP = {
    "sun": "0",
    "mon": "1",
    "tue": "2",
    "wed": "3",
    "thu": "4",
    "fri": "5",
    "sat": "6"
}

SAT = ('*', '*', '*', 'sat', '*')
SUN = ('*', '*', '*', 'sun', '*')

TIME_START_TO_END = {
    'years': {
        'start': 1,
        'end': 9999,
    },
    'months': {
        'start': 1,
        'end': 12,
    },
    'days': {
        'start': 1,
        'end': 31,
    },
    'weeks': {
        'start': 1,
        'end': 7,
    },
    'number_weeks': {
        'start': 1,
        'end': 5,
    },
}


class Holiday(object):
    """
    Base class
    """

    IS_TIMES = set()

    def __init__(self, times):
        """
        :param Tuple of List times: Plz see below
        # ('*', '*', '*', '*', '*')
        #   ┬   ┬   ┬   ┬   ┬
        #   │   │   │   │   │
        #   │   │   │   │   │
        #   │   │   │   │   └─  number of week (1 - 5)
        #   │   │   │   └─── day of week (0 - 7) (0 to 6 are Sunday to Saturday)
        #   │   │   └───── day of month (1 - 31)
        #   │   └─────── month (1 - 12)
        #   └───────── year (0 - 9999)
        :param boolian is_reverse: return the opposite result
        """
        if isinstance(times, list):
            for time in times:
                if isinstance(time, tuple) and len(time) == 5:
                    self.IS_TIMES.add(True)
                else:
                    self.IS_TIMES.add(False)

        if len(self.IS_TIMES) == 1:
            self.years = zip(*times)[0]
            self.months = zip(*times)[1]
            self.days = zip(*times)[2]
            self.weeks = zip(*times)[3]
            self.number_weeks = zip(*times)[4]

    def is_business_day(self, date, is_reverse=False):
        """ get is_business_day

        :param date_object: Exsample >>>date(2000, 1, 1)
        :return: return the result of boolian
        """
        return ""

    def get_period_count_holidays(self, start_date=None, end_date=None):
        """
        """
        return ""

    def _create_data_structure(self):
        """ create_data_structure

        :return: return dict of time name keys and period values
        :Exsample: >>> {"years": [2000, 2001], "months": set([11,12]), ...}
        """

        time_data = {}

        for time_name, v in TIME_START_TO_END.items():

            if '*' in self.__dict__[time_name]:
                time_data[time_name] = range(v["start"], v["end"]+1)
            else:
                period = self._check_time_format(time_name, set(self.__dict__[time_name]))
                time_data[time_name] = period

        return time_data

    def _check_time_format(self, time_name, values):
        """ check time

        :param time name of String time_name: years or months or days or weeks or number week
        :param List of times values: Number or the asterisk in the list
        :return: It returns a value if there is no exception
        """
        period = TIME_START_TO_END[time_name]

        for value in values:
            if not isinstance(value, int):
                raise TypeError("'%s' is not an int" % value)
            if value in range(period["start"], period["end"]+1):
                raise PeriodRangeError("'%d' is outside the scope of the period "
                                       "'%s' range: '%d' to '%d'" % (
                                           value,
                                           time_name,
                                           period["start"],
                                           period["end"]))

        return values


if __name__ == '__name__':
    holiday = Holiday([
        ('*', '*', '*', '*', '*'),
    ])

    print holiday.days
