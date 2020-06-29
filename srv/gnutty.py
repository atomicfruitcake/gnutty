"""!
@author atomicfruitcake

@date 2020

Gnutty Server
"""

from srv.server import Server
from srv import constants
from srv.request_methods import RequestMethods
from srv.exceptions.invalid_method_exception import InvalidMethodException

class Gnutty:
    """
    Gnutty Server class
    """
    
    def __init__(self, host="0.0.0.0", port=constants.PORT):
        """
        Constructor method for gnutty server
        :param host: str - Network interface IP where server will run
        :param port: int - port where the server can be accessed from
        """
        self.host = host
        self.port = port
        self.server = Server(host=self.host, port=self.port)

    def __create_endpoint(self, path, method):
        if method not in vars(RequestMethods).values():
            raise InvalidMethodException(
                "Method {} is not valid".format(method)
            )
        if method == RequestMethods.GET:
            self.server.get(path=path)

    def create_get(self, path):
        self.__create_endpoint(path=path, method=RequestMethods.GET)

