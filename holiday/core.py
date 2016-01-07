# -*- coding: utf-8 -*-
import re
from .exceptions import ParseError

# cron方式もやる？
# TIME_SYNTAX_RE = re.compile(r"^.+\s+.+\s+.+\s+.+$")


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

# Year, Month, Day of Month, Day of Week
SAT = ('*', '*', '*', 'sat')
SUN = ('*', '*', '*', 'sun')


class Holiday(object):
    """
    - base class
    """

    def __init__(self, dates=[], reverse=False):

        self.dates = dates
        self._reverse = reverse

    def is_business_day(self, *args):
        """
        """
        return ""

    def _parse_time():
        """
        """
        return ""

    def _parse_year():
        """
        """
        return ""

    def _parse_month():
        """
        """
        return ""

    def _parse_day():
        """
        """
        return ""


class ParseValues(object):
    """
    """
    pass


holiday = Holiday([SAT, SUN] + [
    ('*', 9, '*', 'mon'),  # 敬老の日
])


holiday.is_business_day()
