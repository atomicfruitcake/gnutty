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

    def __init__(self, host="0.0.0.0", port=constants.PORT, favicon=None):
        """
        Constructor method for gnutty server
        :param host: str - Network interface IP where server will run
        :param port: int - Port where the server can be accessed from
        :param favicon: str - Path to favicon.ico to be used
        """
        self.host = host
        self.port = port
        super(Gnutty, self).__init__(host=self.host, port=self.port)

        self.favicon = (
            os.path.join(Path(os.path.dirname(__file__)).parent, "favicon.ico")
            if not favicon
            else favicon
        )

    def __create_endpoint(self, path: str, method: str):
        """
        Create an endpoint on the nutty server
        """
        if method not in vars(RequestMethods).values():
            raise InvalidMethodException("Method {} is not valid".format(method))

    def create_get(self, path):
        self.__create_endpoint(path=path, method=RequestMethods.GET.value)



def run_gnutty():
    server = Gnutty(port=8000)

    @server.get("/")
    def root(request):
        return Response(body="OK")

    @server.get("/favicon.ico")
    def favicon(request):
        return Response(
            body=open(
                os.path.join(Path(os.path.dirname(__file__)).parent, "favicon.ico"),
                "rb",
            ).read()
        )

    @server.post("/test")
    def new(request):
        print(request)
        response = {
            "msg": "Received request : {}".format(request.body)
        }
        bdy = request.body
        return Response(
            body=request.body
        )
        return 200, request.body

    @server.any()
    def not_found(request):
        return Response(
            code=ResponseCodes.NOT_FOUND.value,
            body="NOT FOUND",
            content_type="text/html",
        )

    server.serve()


if __name__ == "__main__":
    run_gnutty()
