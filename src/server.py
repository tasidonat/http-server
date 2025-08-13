import socket
from utils import parse_request, build_response

def handle_route(method, path, body):
    if path == '/':
        return "200 OK", "Hello World!"
    elif path == '/about':
        return "200 OK", "This is a minimal HTTP/1.1 server."
    elif path == '/data':
        if method == 'POST':
            return "200 OK", f"Received POST data: {body}"
        else:
            return "200 OK", "Send a POST request to /data."
    else:
        return "404 Not Found", "Not Found"

def main():
    HOST, PORT = '', 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Listening on port {PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    request_bytes = b''
                    while True:
                        chunk = conn.recv(1024)
                        request_bytes += chunk
                        if b'\r\n\r\n' in request_bytes or not chunk:
                            break
                    if not request_bytes:
                        break

                    method, path, version, headers, body = parse_request(request_bytes)
                    if not method:
                        response = build_response("400 Bad Request", "Malformed request.", keep_alive=False)
                        conn.sendall(response.encode('utf-8'))
                        break

                    if version == "HTTP/1.1" and 'host' not in headers:
                        response = build_response("400 Bad Request", "Host header required.", keep_alive=False)
                        conn.sendall(response.encode('utf-8'))
                        break

                    keep_alive = headers.get('connection', '').lower() == 'keep-alive'
                    status, resp_body = handle_route(method, path, body)
                    response = build_response(status, resp_body, keep_alive=keep_alive)
                    conn.sendall(response.encode('utf-8'))

                    if not keep_alive:
                        break
if __name__ == "__main__":
    main()