# -*- coding: utf-8 -*-


class ParseDate(object):
    """ parse date object """

    def __init__(self, date):
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.weekday = date.isoweekday()
        self.week_number = _extract_week_number(date)

    def as_dict(self):
        """ date to dict

        :rtype: dict
        :return: times dict
        """

        return {
            "years": self.year,
            "months": self.month,
            "days": self.day,
            "weeks": self.weekday,
            "number_weeks": self.week_number,
        }


def _extract_week_number(date):
    """ get week number """
    first_date = date.replace(day=1)
    return int(date.strftime('%W')) - int(first_date.strftime('%W')) + 1
