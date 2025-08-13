def parse_request(request_bytes):
    try:
        request_text = request_bytes.decode('utf-8')
        lines = request_text.split('\r\n')
        request_line = lines[0]
        method, path, version = request_line.split()
        headers = {}
        i = 1
        while lines[i]:
            key, value = lines[i].split(': ', 1)
            headers[key.lower()] = value
            i += 1
        body = '\r\n'.join(lines[i+1:]) if (i+1) < len(lines) else ''
        return method, path, version, headers, body
    except Exception:
        return None, None, None, {}, ''

def build_response(status, body, keep_alive=False, content_type='text/plain'):
    status_line = f"HTTP/1.1 {status}\r\n"
    headers = [
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body.encode('utf-8'))}",
    ]
    if keep_alive:
        headers.append("Connection: keep-alive")
    else:
        headers.append("Connection: close")
    header_str = '\r\n'.join(headers)
    return f"{status_line}{header_str}\r\n\r\n{body}"