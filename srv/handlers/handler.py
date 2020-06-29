"""!
@author atomicfruitcake

@date 2020
"""

from srv.logger import logger

class Handler:
    """
    Handler Class object
    """
    def can_handle(self, request) -> bool:
        """
        Set whether the handler is able to handle the given response
        :param request: HTTP request object
        :return: bool - True if can handle request, False otherwise
        """
        return False

    def handle(self, request):
        """
        Handle a request to the server
        :param request: HTTP request object
        :raises RuntimeErrror
        """
        raise RuntimeError("abstract")

    @staticmethod
    def log_request(request):
        logger.info(
            "Received {method} request from {sender_ip} to path {path}".format(
                method=request.method,
                sender_ip=request.hostname,
                path=request.path
            )
        )
