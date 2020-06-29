"""!
@author atomicfruitcake

@date 2020
"""

from srv.server import Server
from srv import constants
from srv.request_methods import RequestMethods

class Gnutty(Server):

    def __init__(self, host="0.0.0.0", port=constants.PORT):
        super().__init__(host=host, port=port)

    def create_endpoint(self, path, methods=[RequestMethods.GET]):
        pass

