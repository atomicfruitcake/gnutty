# GNUTTY
Pure Python HTTP Server

# How do I use this?
So long as you have Python3.4 or higher, there are no
dependencies to worry about. Gnutty uses nothing but Python

To start the example server, run
```
python3 ./srv/gnutty.py
```
From the root of the repository.

You can confirm that it is running by opening
`http://127.0.0.1:8000/` in a browser and checking you
receive the plaintext response of `OK`

You can also run
```bash
curl -v http://127.0.0.1:8000
```
To confirm the response from the Gnutty Server
```
~  curl -v http://127.0.0.1:8000
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET / HTTP/1.1
> Host: 127.0.0.1:8000
> User-Agent: curl/7.64.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: Gnutty HTTP server 0.1
< Content-Type: text
< Content-Length: 2
<
* Closing connection 0
OK
```
