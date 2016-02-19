# -*- coding: utf-8 -*-

import unittest
from datetime import date
from holiday.core import Holiday
from holiday.exceptions import ParseError, PeriodRangeError


class TestHoliday(unittest.TestCase):

    def test_with_ok_map_day_of_week(self):
        mon = Holiday([(2015, 12, 28, "mon", 5)])
        tue = Holiday([(2015, 12, 29, "tue", 5)])
        wed = Holiday([(2015, 12, 30, "wed", 5)])
        thu = Holiday([(2015, 12, 31, "thu", 5)])
        fri = Holiday([(2016, 1, 1, "fri", 1)])
        sat = Holiday([(2016, 1, 2, "sat", 1)])
        sun = Holiday([(2016, 1, 3, "sun", 1)])
        self.assertTrue(mon.is_holiday(date(2015, 12, 28)))
        self.assertTrue(tue.is_holiday(date(2015, 12, 29)))
        self.assertTrue(wed.is_holiday(date(2015, 12, 30)))
        self.assertTrue(thu.is_holiday(date(2015, 12, 31)))
        self.assertTrue(fri.is_holiday(date(2016, 1, 1)))
        self.assertTrue(sat.is_holiday(date(2016, 1, 2)))
        self.assertTrue(sun.is_holiday(date(2016, 1, 3)))

    def test_with_ok_asterisk_year(self):
        asterisk = Holiday([("*", 1, 1, "fri", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_month(self):
        asterisk = Holiday([(2016, "*", 1, "fri", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_day(self):
        asterisk = Holiday([(2016, 1, "*", "fri", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_day_of_week(self):
        asterisk = Holiday([(2016, 1, 1, "*", 1)])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_asterisk_num_of_week(self):
        asterisk = Holiday([(2016, 1, 1, "fri", "*")])
        self.assertTrue(asterisk.is_holiday(date(2016, 1, 1)))

    def test_with_ok_bad_holiday(self):
        self.assertRaises(ParseError, lambda: Holiday([(2016, 1, 1, "test", 1)]))
        self.assertRaises(PeriodRangeError, lambda: Holiday([(10000, 1, 1, "fri", 1)]))
        self.assertRaises(PeriodRangeError, lambda: Holiday([(2016, 13, 1, "fri", 1)]))
        self.assertRaises(PeriodRangeError, lambda: Holiday([(2016, 1, 32, "fri", 1)]))
        self.assertRaises(PeriodRangeError, lambda: Holiday([(2016, 1, 1, 8, 1)]))
        self.assertRaises(PeriodRangeError, lambda: Holiday([(2016, 1, 32, "fri", 6)]))


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHoliday)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test()
