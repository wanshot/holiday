# -*- coding: utf-8 -*-

"""
    holiday
    ~~~~~~~
    :copyright: (c) 2016 by wanshot.
    :license: MIT, see LICENSE for more details.

    SpecialThanks
    ~~~~~~~~~~~~~
    @crohaco: The review and gave me an idea
    @tell-k: It taught me pipy debut way

"""

import sys
import unittest

from bday._compat import PY2


class BaseTestCase(unittest.TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def setUp(self):
        self.setup()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.teardown()
