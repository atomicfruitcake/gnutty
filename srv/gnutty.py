"""!
@author atomicfruitcake

@date 2020

Gnutty Server
"""
import os
from pathlib import Path

from srv.gnuttycore import GnuttyCore
from srv import constants
from srv.request_methods import RequestMethods
from srv.exceptions.invalid_method_exception import InvalidMethodException
from srv.response import Response
from srv.response_codes import ResponseCodes

class Gnutty(GnuttyCore):
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
        super(Gnutty, self).__init__(
            host=self.host,
            port=self.port
        )

    def __create_endpoint(self, path: str, method: str):
        """
        Create an endpoint on the nutty server
        """
        if method not in vars(RequestMethods).values():
            raise InvalidMethodException(
                "Method {} is not valid".format(method)
            )
        # if method == RequestMethods.GET:
        #     self.core.get(path=path)

    def create_get(self, path):
        self.__create_endpoint(path=path, method=RequestMethods.GET.value)

    @staticmethod
    def send_image(filepath):
        return 200, open(filepath, "rb").read()

    

def run_gnutty():
    server = Gnutty(port=8000)
    @server.get("/")
    def root(request):
        print(request)
        return Response(
            code=ResponseCodes.OK.value, body="OK", content_type="text/html"
        )

    @server.get("/favicon.ico")
    def favicon(request):
        return server.send_image(
            filepath=os.path.join(
                Path(
                    os.path.dirname(__file__)
                ).parent,
                "favicon.ico"
            )
        )


    @server.post("/test")
    def new(request):
        return 200, request.body

    @server.any()
    def not_found(request):
        return Response(code=ResponseCodes.NOT_FOUND.value, body="NOT FOUND", content_type="text/html")

    server.serve()

if __name__ == "__main__":
    run_gnutty()
