# -*- coding: utf-8 -*-


class BaseError(Exception):
    """
    Baseclass for all Holiday errors.
    """


class ParseError(BaseError):
    """
    Holiday dates value parse error.
    """
