"""!
@author atomicfruitcake

@date 2020

Core HTTP Server. This is the backbone of Gnutty that defines responses to
HTTP __request methods and handles the __request object to return the response
"""
import socket

from srv import constants
from srv.handlers.client_handler import ClientHandler
from srv.handlers.handler import Handler
from srv.logger import logger

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

        def dec(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "GET" and request.path == path

                def handle(self, request):
                    self.log_request(request=request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return dec


    def post(self, path):

        def dec(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "POST" and request.path == path

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return dec


    def patch(self, path):

        def dec(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "PATCH" and request.path == path

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return dec


    def delete(self, path):

        def dec(f):
            class __Handler(Handler):

                def can_handle(self, request):
                    return request.method == "DELETE" and request.path == path

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f
        return dec


    def any(self):

        def dec(f):
            class __Handler(Handler):
                def can_handle(self, request):
                    return True

                def handle(self, request):
                    self.log_request(request)
                    return f(request)

            self.handlers.append(__Handler())
            return f

        return dec


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
        request = client_handler.parse_request()
        response = client_handler.handle_request(request)
        client_handler.send_response(response=response)
