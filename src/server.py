import socket
import uuid
from utils import parse_request, build_response

sessions = {}

def get_or_create_session(headers):
    cookies = headers.get('cookie', '')
    session_id = None
    if cookies:
        for cookie in cookies.split(';'):
            key, _, value = cookie.strip().partition('=')
            if key == 'session_id':
                session_id = value
                break
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {'visits': 0}
        is_new = True
    else:
        is_new = False
    return session_id, is_new

def handle_route(method, path, body, session):
    session['visits'] += 1
    if path == '/':
        return "200 OK", f"Hello World! You have visited {session['visits']} times."
    elif path == '/about':
        return "200 OK", f"This is a minimal HTTP/1.1 server. Session visits: {session['visits']}"
    elif path == '/data':
        if method == 'POST':
            session['last_post'] = body
            return "200 OK", f"Received POST data: {body} (Session visits: {session['visits']})"
        else:
            last = session.get('last_post', 'None')
            return "200 OK", f"Send a POST request to /data. Last POST: {last} (Session visits: {session['visits']})"
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

                    session_id, is_new = get_or_create_session(headers)
                    session = sessions[session_id]

                    status, resp_body = handle_route(method, path, body, session)
                    extra_headers = []
                    if is_new:
                        extra_headers.append(f"Set-Cookie: session_id={session_id}; HttpOnly; Path=/")

                    response = build_response(
                        status,
                        resp_body,
                        keep_alive=keep_alive,
                        content_type='text/plain',
                        extra_headers=extra_headers
                    )
                    conn.sendall(response.encode('utf-8'))

                    if not keep_alive:
                        break
if __name__ == "__main__":
    main()