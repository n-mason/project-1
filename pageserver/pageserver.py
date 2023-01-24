"""
  A trivial web server in Python.

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible.

  This program used to serve an ascii graphic of a cat.
  It has been changed so that now it serves files if they are
  located in ./pages  (where '.' is the directory from which this
  program is run).
"""

import config    # Configure from .ini files and command line
import logging   # Better than print statements
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
# Logging level may be overridden by configuration 

import socket    # Basic TCP/IP communication on the internet
import _thread   # Response computation runs concurrently with main program

import os        # Allows path to file requested to be checked


def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket


def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        log.info("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept()
        _thread.start_new_thread(func, (clientsocket,))


##
# Starter version only serves cat pictures. In fact, only a
# particular cat picture.  This one.
##
CAT = """
     ^ ^
   =(   )=
"""

# HTTP response codes, as the strings we will actually send.
# See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# or    http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
##
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"

def respond(sock):
    """
    This server responds only to GET requests (not PUT, POST, or UPDATE).
    Any valid GET request is answered with the appropriate HTTP response code and body msg.
    """
    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    log.info("--- Received request ----")
    log.info("Request was {}\n***\n".format(request))

    parts = request.split()

    if len(parts) > 1 and parts[0] == "GET":
        #transmit(STATUS_OK, sock)
        """
        log.info("DOCROOT is...")
        log.info(docroot);
        log.info("\n")
        log.info(parts[1]) #ex: pages/trivia.html
        """
        path_split = (parts[1]).rsplit("/")
        #log.info(path_split)
        
        file_to_check = path_split[-1] # Need to check for this file inside of DOCROOT 
        # DOCROOT is defined as the pages/ directory in credentials.ini

        #log.info(file_to_check)
        #log.info("\n")

        if docroot[-1] is "/": # If DOCROOT already ends with a "/", don't concatenate a "/"
            path_to_check = docroot + file_to_check 
        else:
            path_to_check = docroot + "/" + file_to_check
        """
        log.info("Path to check is...")
        log.info(path_to_check)
        log.info("\n")
        """
        
        # If request contains .. or ~ then transmit STATUS_FORBIDDEN followed by info msg in the body
        if (".." in parts[1]) or ("~" in parts[1]):
            transmit(STATUS_FORBIDDEN, sock) 
            forb_bdy_msg = "The characters .. and ~ are forbidden in the client request\n"
            transmit(forb_bdy_msg, sock)

        # Else if file exists in pages/ directory, transmit STATUS_OK followed by file
        elif os.path.isfile(path_to_check):
            transmit(STATUS_OK, sock)
            # Now need to transmit file to sock, so need to open and then send the file contents
            file = open(path_to_check, "r")
            file_contents = file.read()
            transmit(file_contents, sock)
            file.close()

        # Else if file does not exist, transmit STATUS_NOT_FOUND followed by info msg in the body    
        else:
            transmit(STATUS_NOT_FOUND, sock)
            # Now transmit info msg
            not_found_bdy_msg = "The file requested was not found in the pages/ directory\n"
            transmit(not_found_bdy_msg, sock)
            
        #transmit(CAT, sock)
    else:
        log.info("Unhandled request: {}".format(request))
        transmit(STATUS_NOT_IMPLEMENTED, sock)
        transmit("\nI don't handle this request: {}\n".format(request), sock)

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    return


def transmit(msg, sock):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes(msg[sent:], encoding="utf-8")
        sent += sock.send(buff)

###
#
# Run from command line
#
###


def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    # Defaults from configuration files;
    #   on conflict, the last value read has precedence
    options = config.configuration()
    # We want: PORT, DOCROOT, possibly LOGGING

    if options.PORT <= 1000:
        log.warning(("Port {} selected. " +
                         " Ports 0..1000 are reserved \n" +
                         "by the operating system").format(options.port))

    global docroot
    docroot = options.DOCROOT
    return options


def main():
    options = get_options()
    port = options.PORT
    if options.DEBUG:
        log.setLevel(logging.DEBUG)
    sock = listen(port)
    log.info("Listening on port {}".format(port))
    log.info("Socket is {}".format(sock))
    serve(sock, respond)


if __name__ == "__main__":
    main()
