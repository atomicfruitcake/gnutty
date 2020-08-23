"""!
@author atomicfruitcake

@date 2020

Response object for when an authorization check fails
"""

from srv.responses.response import Response
from srv.responses.response_codes import ResponseCodes

class NotAuthorizedResponse(Response):

    def __init__(self):

        super(Response).__init__(
            body="NOT AUTHORIZED",
            code=ResponseCodes.UNAUTHORIZED.value
        )
