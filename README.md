# UOCIS322 - Project 1 #
Name: Nathaniel Mason

Contact Info: nmason@uoregon.edu or nmason0204@gmail.com

Project Description: 
This project is focused on creating some logic for an existing simple webpage server. The logic will check requests and determine if a file exists in the DOCROOT directory or not. The DOCROOT directory is defined in credentials.ini, or if credentials.ini is not defined then default.ini (found in the pageserver directory) is used. The code for the logic is contained in pageserver.py which is found in the pageserver directory. The pageserver directory also contains a configuration parser file which will use the information found in credentials.ini, or default.ini if credentials.ini is not found. 

To start the server, use the 'make start' or 'make run' command (defined in the Makefile)
To stop the server, use the 'make stop' command (also defined in the Makefile). 
Along with defining what directory DOCROOT is, a port number for the server can be defined in credentials.ini.
Additionally, there is a 'make clean' command which will clean up python files created by pageserver.py, and a 'make veryclean' command that will remove the ,pypid file (this file contains the stored process id) that gets created when the server is started.

Once the server is started, to test if a file exists you can use your browser to access the address at the port you specified (for example, ix-dev.cs.uoregon.edu:5002/test.html). Curl could be used to test a request as well. 

If the file specified in the request exists, a 200 OK header will be transmitted and then the content of the file will be displayed.
If the file specified in the request does not exist, a 404 Not Found error code will be transmitted in the header and then a small informational message will be displayed.
If the request contains ".." or "~", a 403 Forbidden error code will be transmitted in the header and then a small informational message will be displayed letting the user know that these characters are not allowed in the requests. 

 
