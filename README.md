# customhttpserver

 This is a custom HTTP server side code(tested on Python 3.7.3) running on a user 
 provided port and which can serve GET requests on one or more custom paths and 
 a custom port, both of which can be provided by the user. If these custom values 
 are not provided at runtime, then the server starts on a default port of 11111
 (provided the port is not held on to by any other process locally yet) and 
 serves on default path "/".

## How to start the server?
   `python customhttpserver.py --port <server-port> --path <comma-separated-server-paths>`

   Example:
   `python customhttpserver.py --port 12345 --path "/foo,/bar"`

   The above example command starts the custom HTTP server on port 12345(assuming no other process is hanging on to that port) and is ready to serve GET requests for paths `/foo` and `/bar`.

