# This is a custom HTTP server side code running on a user given port and which can
# serve GET and POST requests on one or more custom paths and a custom port, both of which
# can be provided by the user. If these custom values are not provided at runtime,
# then the server starts on a default port of 11111(provided the port is not opened
# by any other process locally yet) and serves on default path "/".
#
# How to start the server?
# python customhttpserver.py --port <server-port> --path <comma-separated-server-paths> [--delay <duration>]
#
# Example:
# python customhttpserver.py --port 12345 --path /foo,/bar --delay 6
# This will start the server on port 12345 and serve GET and POST API on endpoints /foo and /bar
# and will respond to requests after a delay of 6 seconds.
#


from http.server import BaseHTTPRequestHandler, HTTPServer
from time import gmtime, strftime, sleep
from optparse import OptionParser
import socket
import json


def get_handler(serving_path, slow_duration=0):
    # This is the factory class implementation returning the appropriate custom handler based on user input
    class MyCustomHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.serving_paths = {}
            self.slow_duration = slow_duration
            # Create a dict with keys as serving path-prefixes
            for path in serving_path.split(','):
                self.serving_paths[path.strip()] = True
            # BaseHTTPRequestHandler init calls do_GET().
            # So set attributes needed by do_GET before calling the super's __init__
            super(MyCustomHandler, self).__init__(*args, **kwargs)

        def _set_json_headers(self):
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_GET(self):
            if self.slow_duration > 0:
                sleep(self.slow_duration)
                
            if self.path in self.serving_paths or self.path.rstrip("/") in self.serving_paths:
                # Set the response code to be sent in the HTTP response
                self.send_response(200)
                self._set_json_headers()
                response_data = {
                    "Server-Hostname": socket.gethostname(),
                    "Current-GMT-Time": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                    "Request-Headers": dict(self.headers)
                }
                self.wfile.write(bytes(json.dumps(response_data), "utf-8"))
                return
            else:
                self.send_response(500)
                self._set_json_headers()

        def do_POST(self):
            if self.slow_duration > 0:
                sleep(self.slow_duration)
                
            if self.path in self.serving_paths or self.path.rstrip("/") in self.serving_paths:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)

                self.send_response(200)
                self._set_json_headers()
                
                try:
                    # Try to parse the input as JSON to return it directly
                    input_json = json.loads(post_data.decode('utf-8'))
                    response_data = input_json
                except:
                    # If not valid JSON, return as string
                    response_data = {"data": post_data.decode('utf-8')}
                
                self.wfile.write(bytes(json.dumps(response_data), "utf-8"))
            else:
                self.send_response(500)
                self._set_json_headers()
                
    return MyCustomHandler


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: python %prog --port <server-port> --path <server-path> [--delay <duration>]")
    parser.add_option("--port", action="store", dest="port",
                      default=11111, help="port to start the server on")
    parser.add_option("--path", action="store", dest="path",
                      default="/", help="One or more(comma-separated) path-prefixes served by the server")
    parser.add_option("--delay", action="store", dest="slow_duration",
                      default=0, type="float", help="Delay response by specified seconds")
    (options, args) = parser.parse_args()
    server_address = ('', int(options.port))
    custom_handler = get_handler(options.path, options.slow_duration)
    server = HTTPServer(server_address, custom_handler)
    print(f"Starting http server on port {options.port} for paths {options.path} with response delay of {options.slow_duration} seconds")
    server.serve_forever()