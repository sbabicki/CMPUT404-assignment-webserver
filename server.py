import SocketServer
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#	 http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright  2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
import re
DEFAULT = "./www/index.html"
		

	
class MyWebServer(SocketServer.BaseRequestHandler):

	#find and return path if it is valid
	def parse_path(self):
		
		# regular expression to extract the first line
		firstLineRE = re.compile('GET (/www/.*) HTTP/1\.(0|1)')
		firstLinePath = firstLineRE.match(self.data)
		
		if (firstLinePath != None):
			return "." + firstLinePath.group(1)
		else:
			return DEFAULT
			
		
	def handle(self):
		
		self.data = self.request.recv(1024).strip()
		
		path = self.parse_path()
			
		# TODO: CATCH EXCEPTION
		f = open(path)
		
		# serve page to client
		self.request.sendall(f.read())
		
		print ("Got a request of: %s\n" % self.data)
		#self.request.sendall("OK")
		#self.request.sendall(self.data.upper())
	


if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	SocketServer.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
	


