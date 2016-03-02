# -*- coding: utf-8 -*-

import unittest
from datetime import date
from holiday.exceptions import (
    ParseError,
    PeriodRangeError,
)


class TestHoliday(unittest.TestCase):
    """ Test Command
    python -m unittest discover
    """

    def _getTargetFunc(self):
        from holiday.core import Holiday
        return Holiday

    def _makeOne(self):
        return self._getTargetFunc()

    def test_with_ok_map_day_of_week(self):

        mon = self._makeOne()([(2015, 12, 28, "mon", 5)])
        tue = self._makeOne()([(2015, 12, 29, "tue", 5)])
        wed = self._makeOne()([(2015, 12, 30, "wed", 5)])
        thu = self._makeOne()([(2015, 12, 31, "thu", 5)])
        fri = self._makeOne()([(2016, 1, 1, "fri", 1)])
        sat = self._makeOne()([(2016, 1, 2, "sat", 1)])
        sun = self._makeOne()([(2016, 1, 3, "sun", 1)])
        self.assertTrue(mon.is_holiday(date(2015, 12, 28)))
        self.assertTrue(tue.is_holiday(date(2015, 12, 29)))
        self.assertTrue(wed.is_holiday(date(2015, 12, 30)))
        self.assertTrue(thu.is_holiday(date(2015, 12, 31)))
        self.assertTrue(fri.is_holiday(date(2016, 1, 1)))
        self.assertTrue(sat.is_holiday(date(2016, 1, 2)))
        self.assertTrue(sun.is_holiday(date(2016, 1, 3)))

    def test_with_ok_asterisk_year(self):
        asterisk = self._makeOne()([("*", 1, 1, "fri", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_month(self):
        asterisk = self._makeOne()([(2016, "*", 1, "fri", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_day(self):
        asterisk = self._makeOne()([(2016, 1, "*", "fri", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_day_of_week(self):
        asterisk = self._makeOne()([(2016, 1, 1, "*", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_num_of_week(self):
        asterisk = self._makeOne()([(2016, 1, 1, "fri", "*")])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ng_exclude_asterisk_and_int_year(self):
        ng_values = [u"×", "test", 1.234]
        for ng in ng_values:
            self.assertRaises(TypeError, lambda: self._makeOne()([(ng, 1, 1, "fri", 1)]))

    def test_with_ng_exclude_asterisk_and_int_month(self):
        ng_values = [u"×", "test", 1.234]
        for ng in ng_values:
            self.assertRaises(TypeError, lambda: self._makeOne()([(2016, ng, 1, "fri", 1)]))

    def test_with_ng_exclude_asterisk_and_int_day(self):
        ng_values = [u"×", "test", 1.234]
        for ng in ng_values:
            self.assertRaises(TypeError, lambda: self._makeOne()([(2016, 1, ng, "fri", 1)]))

    def test_with_ng_exclude_asterisk_and_day_of_week_name(self):
        ng_char_values = [u"×", "test"]
        for ng in ng_char_values:
            self.assertRaises(ParseError, lambda: self._makeOne()([(2016, 1, 1, ng, 1)]))

    def test_with_ng_float_day_of_week(self):
        self.assertRaises(TypeError, lambda: self._makeOne()([(2016, 1, 1, 1.234, 1)]))

    def test_with_ng_exclude_asterisk_and_int_week_of_num(self):
        ng_char_values = [u"×", "test", 1.234]
        for ng in ng_char_values:
            self.assertRaises(TypeError, lambda: self._makeOne()([(2016, 1, 1, "fri", ng)]))

    def test_with_ok_is_business_day(self):
        asterisk = self._makeOne()([(2016, 1, 1, "fri", 1)])
        self.assertFalse(asterisk.is_business_day(date(2016, 1, 1)))

    def test_with_ng_is_business_day(self):
        asterisk = self._makeOne()([(2016, 1, 1, "fri", 1)])
        self.assertTrue(asterisk.is_business_day(date(2016, 1, 2)))

    def test_with_ok_exception_holiday(self):
        self.assertRaises(ParseError, lambda: self._makeOne()([(2016, 1, 1, "test", 1)]))
        self.assertRaises(PeriodRangeError, lambda: self._makeOne()([(10000, 1, 1, "fri", 1)]))
        self.assertRaises(PeriodRangeError, lambda: self._makeOne()([(2016, 13, 1, "fri", 1)]))
        self.assertRaises(PeriodRangeError, lambda: self._makeOne()([(2016, 1, 32, "fri", 1)]))
        self.assertRaises(PeriodRangeError, lambda: self._makeOne()([(2016, 1, 1, 8, 1)]))
        self.assertRaises(PeriodRangeError, lambda: self._makeOne()([(2016, 1, 32, "fri", 6)]))


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHoliday)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
