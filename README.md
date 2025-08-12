# HTTP Server

This project implements a simple HTTP/1.0 server in Python. The server listens on port 8080 and responds with a "Hello, World!" message to any incoming HTTP requests.

## Project Structure

```
http-server
├── src
│   ├── server.py       # Main logic for the HTTP server
│   └── utils.py        # Utility functions for parsing HTTP requests
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
curl http://localhost:8080
```

You should see the response:

```
Hello, World!
```

## Overview

This barebones HTTP server is designed for educational purposes to demonstrate the basic principles of handling HTTP requests and responses. It parses the request line, headers, and optional body from the raw bytes received from the client, providing a foundation for further development and learning about web server functionality.