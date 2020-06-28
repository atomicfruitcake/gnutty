"""!
@author atomicfruitcake

@date 2020

Abstract base exception class from which all custom exception must inherit
"""

from abc import ABC

from srv.logger import logger


class AbstractException(Exception, ABC):
    """
    Abstract Exception class
    """
    def __init__(self, msg=""):
        self.msg = msg
        logger.error(msg)

    def __str__(self):
        return self.msg
