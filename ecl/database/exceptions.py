"""
Exception definitions for RDatabase.
"""
import json
from ecl import exceptions


class HttpException(exceptions.HttpException):
    pass


class NotFoundException(HttpException):
    pass
