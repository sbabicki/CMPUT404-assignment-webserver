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
# 
# 
# File edited by Sasha Babicki (CCID: babicki)

import SocketServer
import re
import os.path

ROOTDIR = "./www"
		
class MyWebServer(SocketServer.BaseRequestHandler):

	# throws a 404 not found error and prints message on screen
	def not_found_404(self):
		
		self.request.sendall("HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" +
		"<!DOCTYPE html><html><h2>404 Not Found</h2>" + 
		"\n\n<h3>The requested URL was not found on this server.</h3></html>")
		
		
	# check and return path if path is valid, else return none
	def check_valid_path(self, path):
		
		validPath = None
		
		# normalize path
		path = os.path.normpath(path)
		
		# path starts with /www
		if (path.startswith(ROOTDIR[1:])):
			if (os.path.exists("." + path)):
				validPath = "." + path
		
		# path doesn't start with /www
		elif (os.path.exists(ROOTDIR + path)):
			validPath = ROOTDIR + path
		
		if (validPath != None):	
			
			# if path is directory (ends with "/"), go to index.html file
			if (os.path.isdir(validPath)):
				if (os.path.exists(validPath + "/index.html")):
					validPath = validPath + "/index.html"
				
				# no file index.html in the directory, can't serve anything
				else: 
					validPath = None
			
		return validPath
		
	
	#find and return path if it is valid
	def parse_path(self):
		
		# regular expression to extract path starting with /www/
		pathRE = re.compile('GET (/.*) HTTP/1\.(0|1)')
		pathMatch = pathRE.match(self.data)
		
		# path starts with /www/
		if (pathMatch != None):
			path = pathMatch.group(1)
			return self.check_valid_path(path)
		
		# regular expression to extract path not starting with /www/
		return None
			
			
	def handle(self):
		
		self.data = self.request.recv(1024).strip()
		
		path = self.parse_path()
		
		# if the path is not valid, throw a 404 not found error
		if (path == None):
			self.not_found_404()
		
		else:	
			
			# open file at specified path
			try: 
				f = open(path)
			
			except IOError:
				print("Unsuccessful file access attempt :(")
				self.not_found_404()
			
			else:
			
				# get mimetype from the path
				mimetypeRE = re.compile('./.*\.(.*)')
				mimetypeMatch = mimetypeRE.match(path)
				mimetype = mimetypeMatch.group(1)
			
				self.request.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/%s\r\n\r\n" %mimetype)
		
				# serve page to client
				self.request.sendall(f.read())
			
				f.close()
		
		# print request info to terminal
		print ("\nGot a request of: \n%s\n\n" % self.data)
		

if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	SocketServer.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
	


