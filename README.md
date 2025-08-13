# HTTP Server

This project implements a simple HTTP/1.1 server in Python. The server listens on port 8080 and demonstrates basic HTTP request parsing, routing, and persistent connections.

## Project Structure

```
http-server
├── src
│   ├── server.py       # Main logic for the HTTP server
│   └── utils.py        # Utility functions for parsing HTTP requests and building responses
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

## Usage

To run the server, execute the following command:

```
python src/server.py
```

The server will start listening on port 8080. You can test it by opening a web browser and navigating to `http://localhost:8080` or by using a tool like `curl`:

```
curl -v -H "Host: localhost" http://localhost:8080/
curl -v -H "Host: localhost" http://localhost:8080/about
curl -v -H "Host: localhost" -d "foo=bar" http://localhost:8080/data
```

You should see responses such as:

```
Hello World!
```

or

```
This is a minimal HTTP/1.1 server.
```

or for POST:

```
Received POST data: foo=bar
```

## Features

- Parses HTTP/1.1 request line, headers, and optional body
- Validates the Host header (required by HTTP/1.1)
- Supports persistent connections with `Connection: keep-alive`
- Handles multiple routes: `/`, `/about`, `/data`
- Basic GET and POST handling
- Returns appropriate status codes and Content-Length

## Overview

This minimal HTTP server is designed for educational purposes to demonstrate the basic principles of handling HTTP/1.1 requests and responses. It provides a foundation for further development and learning about web server functionality, including routing, header validation, and persistent connections.