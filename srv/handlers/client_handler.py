"""!
@author atomicfruitcake

@date 2020

Handle HTTP requests and format for client response
"""

from socket import gethostname

from srv.exceptions.no_handler_exception import NoHandlerException
from srv.request import Request
from srv.response import Response
from srv.response_codes import ResponseCodes


class ClientHandler:
    def __init__(self, socket, handlers):
        self.socket = socket
        self.handlers = handlers

    def parse_request(self):
        """
        Parse a request received on the open socket
        """
        raw = self.socket.recv(2048).decode().splitlines()
        method, path, http_version = raw.pop(0).split()
        return Request(
            body="\n".join(raw),
            headers=self.parse_headers(raw),
            method=method,
            path=path,
            hostname=gethostname(),
            http_version=http_version[len("HTTP/"):]
        )

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
        self.send_headers(content_type, body)
        self.socket.send(body)
        return True

    def __send_header(self, name, value):
        self.socket.send("{}: {}\r\n".format(name, value).encode())

    def send_headers(self, content_type, body):
        self.__send_header("Server", "Gnutty HTTP server 0.1")
        self.__send_header("Content-Type", content_type)
        self.__send_header("Content-Length", len(body))
        self.socket.send(b"\r\n")


