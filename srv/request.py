"""!
@author atomicfruitcake

@date 2020

HTTP Request object
"""
from ast import literal_eval


from srv.irequest import IRequest

class Request(IRequest):

    def __init__(self, request):
        """
        Constructor method for the Request object
        :param request:
        """
        self.__request = request

    @property
    def content_type(self):
        return self.__request.content_type

    @property
    def content_length(self):
        return self.__request.content_length

    @property
    def path(self):
        return self.__request.path


    @property
    def method(self):
        return self.__request.method

    @property
    def body(self):
        if self.content_type == "application/json":
            return literal_eval(self.__request.body)
        else:
            return self.__request.body
