"""!
@author atomicfruitcake

@date 2020

Handle HTTP requests and format for client response
"""

from srv.request import Request
from srv.exceptions.no_handler_exception import NoHandlerException
from srv.response_codes import ResponseCodes


class ClientHandler:
    def __init__(self, socket, handlers):
        self.socket = socket
        self.handlers = handlers

    def parse_request(self):
        raw_request = self.socket.recv(2048).decode().splitlines()
        request = Request()
        first_line = raw_request.pop(0)
        request.method, request.path, request.http_version = first_line.split()
        request.http_version = request.http_version[len("HTTP/"):]

        request.headers = self.parse_headers(raw_request)
        request.body = "\n".join(raw_request)

        return request

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

    def send_response(self, response):
        """
        Send an HTTP response object to the client
        :param response:
        :return:
        """
        if isinstance(response, str):
            code = ResponseCodes.OK.value
            body = response
        else:
            code, body = response
        body = body.encode()

        code_name = ResponseCodes(code).name

        self.socket.send("HTTP/1.0 {} {}\r\n".format(code, code_name).encode())

        self.send_header("Server", "Python HTTP server 0.1")
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(body))

        self.finish_headers()
        self.socket.send(body)

    def send_header(self, name, value):
        self.socket.send("{}: {}\r\n".format(name, value).encode())

    def finish_headers(self):
        self.socket.send(b"\r\n")
