# -*- coding: utf-8 -*-
import re
from .exceptions import ParseError

# cron方式もやる？
# http://www.nncron.ru/help/EN/working/cron-format.html
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

    def __init__(self, dates=[], is_reverse=False):

        self.dates = dates
        self._is_reverse = is_reverse

    def is_business_day(self, *args):
        """
        """
        return ""

    def get_term_count_holidays(self, start_date, end_date):
        """
        """
        return ""

    def _parse_dates(self):
        """
        """
        return ""

    def _parse_year(self):
        """
        """
        return ""

    def _parse_month(self):
        """
        """
        return ""

    def _parse_day(self):
        """
        """
        return ""


holiday = Holiday([SAT, SUN] + [
    ('*', 9, '*', 'mon'),  # 敬老の日
])


holiday.is_business_day()
