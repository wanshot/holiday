# -*- coding: utf-8 -*-
from datetime import date as _date


class ParseDate(object):

    def __init__(self, date):
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.weekday = date.weekday()
        self.number_week = self.extract_week_number(date)

    def __repr__(self):
        return ""

    def __call__(self):
        return ""

    def extract_week_number(self, date):
        return u''

# if __name__ == "__main__":
