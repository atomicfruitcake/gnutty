"""!
@author atomicfruitcake

@date 2020
"""
from abc import ABC, abstractmethod

from srv.logger import logger

class Handler(ABC):
    """
    Handler Class object
    """
    def can_handle(self, request) -> bool:
        """
        Set whether the handler is able to handle the given response
        :param request: HTTP __request object
        :return: bool - True if can handle __request, False otherwise
        """
        return False

    @abstractmethod
    def handle(self, request):
        """
        Handle a __request to the server
        :param request: HTTP __request object
        :raises RuntimeError
        """
        raise RuntimeError("abstract")

    @staticmethod
    def log_request(request):
        logger.info(
            "Received {method} __request from {sender_ip} to path {path}".format(
                method=request.method,
                sender_ip=request.hostname,
                path=request.path
            )
        )
