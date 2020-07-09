"""!
@author atomicfruitcake

@date 2020

HTTP Response object
"""

from srv.response_codes import ResponseCodes

class Response:
    """
    HTTP Response object class
    """
    def __init__(self, body, code=ResponseCodes.OK.value, content_type="text/html"):
        if not content_type:
            content_type = "text/html"
        self.body = self.encode_body(body)
        self.code = code
        self.content_type = content_type

    @property
    def head(self):
        return "HTTP/1.0 {code} {codename}\r\n".format(
            code=self.code,
            codename=ResponseCodes(self.code).name
        ).encode()

    @property
    def headers(self):
        return [
            "Server: Gnutty HTTP server 0.1\r\n".encode(),
            "Content-Type: {}\r\n".format(self.content_type).encode(),
            "Content-Length: {}\r\n".format(len(self.body)).encode(),
        ]

    @staticmethod
    def encode_body(body):
        if type(body) is str:
            return body.encode()
        if type(body) is dict:
            return body
        else:
            assert type(body) is bytes
            return body


    def send(self, socket):
        socket.send(self.head)
        [
            socket.send(header)
            for header in
            self.headers
        ]
        socket.send(b"\r\n")
        socket.send(self.body)


