"""!
@author atomicfruitcake

@date 2020

Gnutty Server
"""

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
        super(Gnutty, self).__init__()
        self.host = host
        self.port = port
        self.core = GnuttyCore(host=self.host, port=self.port)

    def __create_endpoint(self, path: str, method: str):
        """
        Create an endpoint on the nutty server
        """
        if method not in vars(RequestMethods).values():
            raise InvalidMethodException(
                "Method {} is not valid".format(method)
            )
        if method == RequestMethods.GET:
            self.core.get(path=path)

    def create_get(self, path):
        self.__create_endpoint(path=path, method=RequestMethods.GET.value)

def test_gnutty():
    server = Gnutty(port=8000)
    server.create_get("/")


    @server.get("/")
    def root(request):
        # return 200, "OK"
        return Response(
            code=ResponseCodes.OK.value, body="OK", content_type="text/html"
        )

    @server.get("/favicon.ico")
    def root(request):
        return Response()

    @server.post("/test")
    def new(request):
        return 200, request.body

    @server.any()
    def not_found(request):
        return Response(code=ResponseCodes.NOT_FOUND.value, body="NOT FOUND", content_type="text/html")

    if __name__ == "__main__":
        server.serve()
