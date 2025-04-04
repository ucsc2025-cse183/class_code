import os
import sys
import socket
import traceback
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs


# IP4 address: 127.0.0.1
# TCP/IP address: 127.0.0.1:80

MIME_OPTIONS = {
    "jpeg": "image/jpeg",
    "txt": "text/plain",
    "html": "text/html",
}

def add(data):
    print(data)
    c = float(data["a"][0]) + float(data["b"][0])
    return str(c)

def date():
    now = datetime.now(timezone.utc)
    timestamp = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return timestamp

def mime(filename):
    extension = filename.split(".")[-1] # cat.jpeg -> jpeg
    return MIME_OPTIONS.get(extension, "text/plain")

def process_request(request):
    lines = request.split("\n")
    first_line = lines[0] # GET /hello/world?a=1&b=2 HTTP/1.1
    method, name, protocol = first_line.split()
    if "?" in name:
        path_info, query_string = name.split("?", 1)
    else:
        path_info, query_string = name, ""
    print("method", method)
    print("protocol", protocol)
    print("path_info", path_info)
    print("query_string", query_string)

    if path_info == "/add":        
        content = add(parse_qs(query_string)).encode()
        content_type = "text/plain"
    else:
        filename = os.path.join("static", path_info[1:])
        if not os.path.exists(filename):
            return b"HTTP/1.1 404 Not Found\r\n\r\n"

        with open(filename, "rb") as stream:
            content = stream.read()
        content_type = mime(filename)

    response = f"""HTTP/1.1 200 OK
Date: {date()}
Server: Apache/2.2.14 (Win32)
Last-Modified: {date()}
Content-Type: {content_type}
Content-Length: {len(content)}

""".encode() + content
    return response

def catch_error(request):
    try:
        response = process_request(request)
    except Exception:
        print(traceback.format_exc())
        response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"  
    return response          

def main(address):
    ip, port = address.split(":")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, int(port)))      # address and port of the server
    sock.listen(1)                  # queue not more than 1 request
    while True:
        conn, addr = sock.accept()  # accept a request for connection
        print(addr)                          # print address of client connecting
        request = conn.recv(1000).decode()   # receive message (http request)
        response = catch_error(request)
        conn.send(response)         # send message (http response)


if __name__ == "__main__":
    main(sys.argv[1])