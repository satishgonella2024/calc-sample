#!/usr/bin/env python3
"""
Simple Web Calculator Application
A standalone Python script that provides a web-based calculator interface.
"""

import argparse
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json


class CalculatorHandler(BaseHTTPRequestHandler):
    """HTTP request handler for calculator operations."""

    def do_GET(self):
        """Handle GET requests - serve the calculator HTML interface."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        """Handle POST requests - perform calculations."""
        if self.path == '/calculate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode())
                result = self.calculate(data)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'result': result}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_error(404, "Endpoint not found")

    def calculate(self, data):
        """Perform the calculation based on the provided data."""
        num1 = float(data.get('num1', 0))
        num2 = float(data.get('num2', 0))
        operation = data.get('operation', '+')

        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ValueError("Division by zero is not allowed")
            return num1 / num2
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def get_html(self):
        """Return the HTML content for the calculator interface."""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Web Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        input, select, button { margin: 10px 0; padding: 10px; width: 100%; box-sizing: border-box; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        #result { margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 5px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>Web Calculator</h1>
    <input type="number" id="num1" placeholder="First number" step="any">
    <select id="operation">
        <option value="+">Addition (+)</option>
        <option value="-">Subtraction (-)</option>
        <option value="*">Multiplication (*)</option>
        <option value="/">Division (/)</option>
    </select>
    <input type="number" id="num2" placeholder="Second number" step="any">
    <button onclick="calculate()">Calculate</button>
    <div id="result"></div>

    <script>
        function calculate() {
            const num1 = document.getElementById('num1').value;
            const num2 = document.getElementById('num2').value;
            const operation = document.getElementById('operation').value;

            fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num1, num2, operation })
            })
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('result');
                if (data.error) {
                    resultDiv.innerHTML = '<span class="error">Error: ' + data.error + '</span>';
                } else {
                    resultDiv.innerHTML = '<strong>Result:</strong> ' + data.result;
                }
            })
            .catch(error => {
                document.getElementById('result').innerHTML = '<span class="error">Error: ' + error + '</span>';
            });
        }
    </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description='Simple Web Calculator Application')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    parser.add_argument('--host', type=str, default='localhost', help='Host to bind to (default: localhost)')
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), CalculatorHandler)
    print(f"Starting calculator server on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    main()