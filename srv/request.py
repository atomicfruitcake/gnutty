"""!
@author atomicfruitcake

@date 2020

HTTP Request object
"""

from srv.methods import METHODS

class Request:

    def __init__(
        self,
        body,
        headers,
        method,
        path,
        hostname,
        content_type="application/json",
        http_version=1.0,
    ):
        self.body = body
        self.headers = headers
        self.method = self.validate_method(method)
        self.path = path
        self.hostname = hostname
        self.content_type = content_type
        self.http_version = http_version

    @property
    def content_length(self):
        return len(self.body)

    @staticmethod
    def validate_method(method):
        assert method.upper() in METHODS
        return method.upper()
