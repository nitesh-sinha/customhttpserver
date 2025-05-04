# customhttpserver

 This is a custom HTTP server side code(tested on `Python 3.7+`) running on a user 
 provided port and exposes GET and POST endpoints on one or more custom paths. User can provide custom port or this service can run on a default port(of 11111) if none is provided.

## How to start the server?
   ```bash
  python customhttpserver.py --port <server-port> --path <comma-separated-server-paths> [--delay <response-delay>]
   ```  

   Example:

    python customhttpserver.py --port 12345 --path "/foo,/bar" --delay 4

   The above example command starts the custom HTTP server on port 12345(assuming no other process is hanging on to that port) and is ready to serve GET and POST requests for paths `/foo` and `/bar`. 
   The service will respond to all requests after a delay of 4 seconds(after receiving the input HTTP request).

