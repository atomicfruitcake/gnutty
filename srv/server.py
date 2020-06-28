"""!
@author atomicfruitcake

@date 2020
"""

import socket

from srv.logger import logger
from srv.handlers.handler import Handler
from srv.handlers.client_handler import ClientHandler
from srv import constants

class Server:
    """
    HTTP server
    """
    def __init__(self, host="0.0.0.0", port=constants.PORT):
        logger.info("Starting Gnutty server on port {}".format(constants.PORT))
        self.socket = socket.socket()
        server_addr = host, port
        self.socket.bind(server_addr)
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def get(self, path):
        def decorator(f):
            class DynamicHandler(Handler):
                def can_handle(self, request):
                    return request.method == "GET" and request.path == path
                def handle(self, request):
                    return f(request)
            self.handlers.append(DynamicHandler())
            return f
        return decorator

    def post(self, path):
        def decorator(f):
            class DynamicHandler(Handler):
                def can_handle(self, request):
                    return request.method == "POST" and request.path == path
                def handle(self, request):
                    return f(request)
            self.handlers.append(DynamicHandler())
            return f
        return decorator

    def any(self):
        def decorator(f):
            class DynamicHandler(Handler):
                def can_handle(self, request):
                    return True
                def handle(self, request):
                    return f(request)
            self.handlers.append(DynamicHandler())
            return f
        return decorator

    def serve_forever(self):
        self.socket.listen()
        while True:
            s2, client_addr = self.socket.accept()
            try:
                self.handle_client(s2)
            except:
                try:
                    s2.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")
                except:
                    pass  # the socket has died, do nothing
            finally:
                s2.close()

    def handle_client(self, socket):
        client_handler = ClientHandler(socket, self.handlers)
        request = client_handler.parse_request()
        response = client_handler.handle_request(request)
        client_handler.send_response(response)


class ToDo:
    def __init__(self):
        self.list = []

    def render_html(self):
        res = "<ul>"
        for item in self.list:
            res += "<li>" + item + "</li>"
        res += "</ul>"
        return res

    def add(self, item):
        self.list.append(item)


server = Server(port=8000)
todo_list = ToDo()


@server.get("/")
def root(request):
    return """
        <html>
            <head>
                <title>To-do list</title>
            </head>
            <body>
                <p>Your to-do list:</p>
                {}
                <form action="/new" method="post">
                    <p>Add a new item:</p>
                    <input type="text" name="name" placeholder="Do stuff"/>
                    <input type="submit" value="Add"/>
                </form>
            </body>
        </html>""".format(todo_list.render_html())


@server.post("/new")
def new(request):
    new_todo = request.body.strip()
    new_todo = new_todo[len("name="):].replace("+", " ")
    todo_list.add(new_todo)
    return 201, "<html><body>Created! Go back to the <a href="/">frontpage</a>.</body></html>"


@server.any()
def not_found(request):
    return 404, "<html><body><font color='red'>Not Found</font></body></html>"

if __name__ == "__main__":
    server.serve_forever()
