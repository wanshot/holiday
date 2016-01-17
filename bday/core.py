# -*- coding: utf-8 -*-
from .exceptions import ParseError, PeriodRangeError
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

    _IS_TIMES = []

    def __init__(self, times):
        """
        :param Tuple of List times: Plz see below
        # ('*', '*', '*', '*', '*')
        #   ┬   ┬   ┬   ┬   ┬
        #   │   │   │   │   │
        #   │   │   │   │   │
        #   │   │   │   │   └─  number of week (1 - 5)
        #   │   │   │   └─── day of week (1 to 7 are Sunday to Saturday)
        #   │   │   └───── day of month (1 - 31)
        #   │   └─────── month (1 - 12)
        #   └───────── year (1 - 9999)
        :param boolian is_reverse: return the opposite result
        """

        if isinstance(times, list):
            for time in times:
                if isinstance(time, tuple) and len(time) == 5:
                    self._IS_TIMES.append(True)
                else:
                    self._IS_TIMES.append(False)

        if all(self._IS_TIMES):
            self.years = zip(*times)[0]
            self.months = zip(*times)[1]
            self.days = zip(*times)[2]
            self.weeks = zip(*times)[3]
            self.number_weeks = zip(*times)[4]

    def is_business_day(self, date):
        """ whether business day

        :param date_object: Exsample >>>date(2000, 1, 1)
        :return: return the result of boolian
        :rtype: boolian
        """

        parsed_date = ParseDate(date).as_dict()
        data = self._create_data_structure()

        if len([v for k, v in parsed_date.items() if v in data[k]]) == 5:
            return True

        return False

    def _create_data_structure(self):
        """ create_data_structure

        :return: return dict of time name keys and period values
        :rtype: dict
        :Exsample: >>> {"years": [2000, 2001], "months": set([11,12]), ...}
        """

        time_data = {}

        for time_name, v in TIME_START_TO_END.items():

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

        period = TIME_START_TO_END[time_name]

        for value in values:

            if not isinstance(value, int):
                raise TypeError("'%s' is not an int" % value)

            if value not in range(period["start"], period["end"]+1):
                raise PeriodRangeError("'%d' is outside the scope of the period "
                                       "'%s' range: '%d' to '%d'" % (
                                           value,
                                           time_name,
                                           period["start"],
                                           period["end"]))

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

        if not len(exclude_weeks):
            return checked_weeks

        raise ParseError("The value could not be Perth")
