# This is a custom HTTP server side code running on a user given port and which can
# serve GET requests on one or more custom paths and a custom port, both of which
# can be provided by the user. If these custom values are not provided at runtime,
# then the server starts on a default port of 11111(provided the port is not opened
# by any other process locally yet) and serves on default path "/".
#
# How to start the server?
# python customhttpserver.py --port <server-port> --path <comma-separated-server-paths>
#
# Example:
# python customhttpserver.py --port 12345 --path /foo,/bar
#

from http.server import BaseHTTPRequestHandler, HTTPServer
from time import gmtime, strftime
from optparse import OptionParser
import socket


def get_handler(serving_path):
    # This is the factory class implementation returning the appropriate custom handler based on user input
    class MyCustomHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.serving_paths = {}
            # Create a dict with keys as serving path-prefixes
            for path in serving_path.split(','):
                self.serving_paths[path.strip()] = True
            # BaseHTTPRequestHandler init calls do_GET().
            # So set attributes needed by do_GET before calling the super's __init__
            super(MyCustomHandler, self).__init__(*args, **kwargs)

        def _set_headers(self):
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

        def do_GET(self):
            if self.path in self.serving_paths or self.path.rstrip("/") in self.serving_paths:
                # Set the response code to be sent in the HTTP response
                self.send_response(200)
                self._set_headers()
                self.wfile.write(bytes("\nServer-Hostname: " + socket.gethostname(), "utf-8"))
                self.wfile.write(bytes("\nCurrent-GMT-Time: " +
                                       strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n", "utf-8"))
                # Echo input HTTP request headers in response body
                self.wfile.write(bytes(self.headers))
                return
            else:
                self.send_response(500)
                self._set_headers()
    return MyCustomHandler


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: python %prog --port <server-port> --path <server-path>")
    parser.add_option("--port", action="store", dest="port",
                      default=11111, help="port to start the server on")
    parser.add_option("--path", action="store", dest="path",
                      default="/", help="One or more(comma-separated) path-prefixes served by the server")
    (options, args) = parser.parse_args()
    server_address = ('', int(options.port))
    custom_handler = get_handler(options.path)
    server = HTTPServer(server_address, custom_handler)
    print("Starting http server on port " + options.port + " and for paths " + options.path)
    server.serve_forever()
