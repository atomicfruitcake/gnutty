"""!
@author atomicfruitcake

@date 2020

Handle HTTP requests and format for client response
"""

from socket import gethostname

from srv.exceptions.no_handler_exception import NoHandlerException
from srv.request import IRequest
from srv.response import Response
from srv.response_codes import ResponseCodes


class ClientHandler:
    def __init__(self, socket, handlers):
        self.socket = socket
        self.handlers = handlers

    def parse_request(self):
        """
        Parse a __request received on the open socker
        """
        raw_request = self.socket.recv(2048).decode().splitlines()
        irequest = IRequest()
        irequest.method, irequest.path, irequest.http_version = raw_request.pop(0).split()
        irequest.http_version = irequest.http_version[len("HTTP/"):]
        irequest.headers = self.parse_headers(raw_request)
        irequest.body = "\n".join(raw_request)
        irequest.hostname = gethostname()
        # TODO Get content type to interface
        # irequest.content_type = raw_request.content_type


        return irequest

    @staticmethod
    def parse_headers(raw_request):
        headers = dict()
        while True:
            line = raw_request.pop(0)
            if not line:
                # reached the end of headers
                break
            name, colon, value = line.partition(": ")
            headers[name] = value
        return headers

    def handle_request(self, request):
        for handler in self.handlers:
            if handler.can_handle(request):
                return handler.handle(request)
        raise NoHandlerException()

    def send_response(self, response, content_type="text/html"):
        """
        Send an HTTP response object to the client
        :param response: HTTP Response object
        """
        if isinstance(response, str):
            code = ResponseCodes.OK.value
            body = response
        elif isinstance(response, Response):
            response.send(socket=self.socket)
            return True
        else:
            code, body = response

        if type(body) is not bytes:
            body = body.encode()

        self.socket.send(
            "HTTP/1.0 {code} {codename}\r\n".format(
                code=code,
                codename=ResponseCodes(code).name
            ).encode()
        )
        self.send_header("Server", "Gnutty HTTP server 0.1")
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(body))

        self.finish_headers()
        self.socket.send(body)
        return True

    def send_header(self, name, value):
        self.socket.send("{}: {}\r\n".format(name, value).encode())

    def finish_headers(self):
        self.socket.send(b"\r\n")
