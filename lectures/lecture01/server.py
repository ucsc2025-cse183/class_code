import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 8002))  # address and port of the server
sock.listen(1)                  # queue not more than 1 request
while True:
    conn, addr = sock.accept()  # accept a request for connection
    print(addr)                 # print address of client connecting
    print(conn.recv(1000))      # receive message (http request)
    print("\n\n\n")              
    response = b"""HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache/2.2.14 (Win32)
Last-Modified: Tue, 01 Jul 2025 19:15:56 GMT
Content-Length: 12

Hello CSE183"""
    conn.send(response)         # send message (http response)
