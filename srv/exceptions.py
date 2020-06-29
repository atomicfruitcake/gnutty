"""!
@author atomicfruitcake

@date 2020

Custom Exception classes
"""

from srv.logger import logger

class InvalidMethodException(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        logger.error(msg)

    def __str__(self):
        return self.msg
