"""!
@author atomicfruitcake

@date 2020

HTTP Response Codes class
"""

from enum import IntEnum

class ResponseCodes(IntEnum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 400
    INTERNAL_SERVER_ERROR = 500
