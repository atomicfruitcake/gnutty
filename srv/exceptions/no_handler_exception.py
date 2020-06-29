"""!
@author atomicfruitcake

@date 2020

Exception class for when a request has no associated rotating_file_handler
"""
from .abstract_exception import AbstractException

class NoHandlerException(AbstractException):
    pass
