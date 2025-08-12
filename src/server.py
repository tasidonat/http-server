import socket

HOST, PORT = '', 8080

def parse_request(request_data):
    request_lines = request_data.split(b'\r\n')
    request_line = request_lines[0].decode('utf-8')
    headers = {}
    
    for line in request_lines[1:]:
        if line:
            key, value = line.decode('utf-8').split(': ', 1)
            headers[key] = value
            
    return request_line, headers

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on PORT {PORT} ...')

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    
    request_line, headers = parse_request(request_data)
    print(f'Request Line: {request_line}')
    print(f'Headers: {headers}')

    http_response = b"""\
HTTP/1.0 200 OK

Hello, World!
"""

    client_connection.sendall(http_response)
    client_connection.close()