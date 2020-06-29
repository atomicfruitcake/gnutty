"""!
@author atomicfruitcake

@date 2020

Core HTTP Server. This is the backbone of Gnutty that defines responses to
HTTP request methods and handles the request object to return the response
"""

import socket

from srv.logger import logger
from srv.handlers.handler import Handler
from srv.handlers.client_handler import ClientHandler
from srv.response_codes import ResponseCodes
from srv import constants
from srv.response import Response

class GnuttyCore:

    def __init__(self, host="0.0.0.0", port=constants.PORT):
        logger.info("Starting Gnutty server on port {}".format(port))
        self.sock = socket.socket()
        server_addr = host, port
        self.sock.bind(server_addr)
        self.handlers = []


    def add_handler(self, handler):
        logger.info("Adding {} handler to Gnutty server")
        self.handlers.append(handler)



    def get(self, path):

        def decorator(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "GET" and request.path == path

                def handle(self, request):
                    self.log_request(request=request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return decorator


    def post(self, path):

        def decorator(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "POST" and request.path == path

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return decorator


    def patch(self, path):

        def decorator(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "PATCH" and request.path == path

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return decorator


    def delete(self, path):

        def decorator(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "DELETE" and request.path == path

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f
        return decorator


    def any(self):

        def decorator(f):
            class __Handler(Handler):
                def can_handle(self, request):
                    return True

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return decorator


    def serve(self):
        self.sock.listen()
        while True:
            _sock, client_addr = self.sock.accept()
            try:
                self.handle_client(_sock)
            except Exception as e:
                logger.warning(e)
                try:
                    _sock.send("500")
                except Exception as e:
                    raise e
            finally:
                _sock.close()


    def handle_client(self, sock):
        client_handler = ClientHandler(sock, self.handlers)
        client_handler.send_response(
            client_handler.handle_request(
                client_handler.parse_request()
            )
        )


server = GnuttyCore(port=8000)


@server.get("/")
def root(request):
    return "OK"

@server.get("/favicon.ico")
def root(request):
    return "OK"


@server.post("/test")
def new(request):
    return 200, request.body


@server.any()
def not_found(request):
    return Response(
        socket=socket.socket(),
        code=ResponseCodes.NOT_FOUND.value,
        body="NOT FOUND",
        content_type="text"
    )

if __name__ == "__main__":
    server.serve()