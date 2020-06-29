"""!
@author atomicfruitcake

@date 2020

Exception for when HTTP Request method is not valid
"""
from .abstract_exception import AbstractException

class InvalidMethodException(AbstractException):
    pass
