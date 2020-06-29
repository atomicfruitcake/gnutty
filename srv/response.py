"""!
@author atomicfruitcake

@date 2020

HTTP Response object
"""

from srv.response_codes import ResponseCodes

class Response:

    def __init__(self, socket, body, code=ResponseCodes.OK.value, content_type=None):
        self.socket = socket
        self.body = body
        self.code = code
        self.content_type = content_type

    def send(self):
        self.socket.send(
            "HTTP/1.0 {code} {codename}\r\n".format(
                code=self.code, codename=ResponseCodes(self.code).name
            ).encode()
        )
        self.send_header("Server", "Gnutty HTTP server 0.1")
        if self.content_type:
            self.send_header("Content-Type", self.content_type)
        self.send_header("Content-Length", len(self.body))
        self.socket.send(b"\r\n")
        self.socket.send(self.body)


    def send_header(self, name, value):
        self.socket.send("{}: {}\r\n".format(name, value).encode())
