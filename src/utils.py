def parse_request(request_bytes):
    request_text = request_bytes.decode('utf-8')
    request_line, *headers = request_text.split('\r\n')
    headers = {header.split(': ')[0]: header.split(': ')[1] for header in headers if ': ' in header}
    
    return request_line, headers

def extract_body(request_bytes):
    request_text = request_bytes.decode('utf-8')
    body = request_text.split('\r\n\r\n', 1)
    return body[1] if len(body) > 1 else ''