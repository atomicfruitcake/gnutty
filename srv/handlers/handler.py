"""!
@author atomicfruitcake

@date 2020

Abstract HTTP Request handler class from which all handlers must inherit
"""

from abc import ABC, abstractmethod

from srv.logger import logger
from srv.request import Request


class Handler(ABC):
    """
    Handler Class object
    """
    def can_handle(self, request: Request) -> bool:
        """
        Set whether the handler is able to handle the given response
        :param request: HTTP __request object
        :return: bool - True if can handle __request, False otherwise
        """
        return False

    @abstractmethod
    def handle(self, request: Request):
        """
        Handle a __request to the server
        :param request: HTTP __request object
        :raises RuntimeError
        """
        raise RuntimeError("abstract")

    @staticmethod
    def log_request(request: Request):
        logger.info(
            "Received {method} __request from {sender_ip} to path {path}".format(
                method=request.method,
                sender_ip=request.hostname,
                path=request.path
            )
        )

