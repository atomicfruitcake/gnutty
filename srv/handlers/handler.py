"""!
@author atomicfruitcake

@date 2020
"""

class Handler:
    """
    Handler Class object
    """
    def can_handle(self, request):
        return False

    def handle(self, request):
        """
        Handle a request to the server
        :param request: HTTP request object
        :raises RuntimeErrror
        """
        raise RuntimeError("abstract")
