from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from data import dataDB
import json
import datetime

# paragraphs = []
class MyHandler (BaseHTTPRequestHandler):
	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		self.end_headers()
		return
	def do_GET(self):
		print("Path:", self.path)
		if self.path == "/messages": #path for the request
			self.handleList()
		elif self.path.startswith("/messages/"):
			parts = self.path.split("/")
			fourm_id = parts[2]
			self.handleFourmRetrieve(fourm_id)
		else: 
			self.handleNotFound() 

	def do_POST(self):
		if self.path == "/messages":
			self.handleCreate()
		else:
			self.handleNotFound()
			
	def do_PUT(self):
		if self.path.startswith("/messages/"):
			parts = self.path.split("/")
			fourm_id = parts[2]
			self.handleFourmUpdate(fourm_id)
		else: 
			self.handleNotFound()

	def do_DELETE(self):
		if self.path.startswith("/messages/"):
			parts = self.path.split("/")
			fourm_id = parts[2]
			self.handleFourmDelete(fourm_id)
		else: 
			self.handleNotFound()


	def handleFourmDelete(self, fourm_id):
		db = dataDB()
		post = db.getfourm(fourm_id)

		if post == None:
			self.handleNotFound()
		else:
			db.deletefourm(fourm_id)
			self.send_response(200)
			self.send_header("Access-Control-Allow-Origin", "*") #star means all orgins
			self.end_headers() #puts ribbon on the request and send it

	def handleFourmUpdate(self, fourm_id):
		db = dataDB()
		post = db.getfourm(fourm_id)

		if post == None:
			self.handleNotFound()
		else:
			length = self.headers["Content-length"]

			#read the body data from the client
			body = self.rfile.read(int(length)).decode("utf-8") #recieve data from client
			#print("the body:",body) #body is firstname=dj&lastnaame=holt

			data = parse_qs(body) #parse query string(qs)
			#print("the data:", data)

			name = data['name'][0]
			age = data['age'][0]
			sentence = data['sentence'][0] #data works as a dictonary with a list of values.
			date = data['date'][0]
			ten = data['ten'][0]

			sentence = sentence.replace("\n", " ")
			db.updatefourm(fourm_id, name, age, sentence, date, ten)
			self.send_response(200)
			self.send_header("Access-Control-Allow-Origin", "*") #star means all orgins
			self.end_headers() #puts ribbon on the request and send it
			

	def handleFourmRetrieve(self, fourmID):
		db = dataDB()
		post = db.getfourm(fourmID)

		if post == None:
			self.handleNotFound()
		else:
			self.send_response(200)
			self.send_header("Content-type", "application/json") #put in headers. This is also a MIME type
			self.send_header("Access-Control-Allow-Origin", "*") #star means all orgins
			self.end_headers() #puts ribbon on the request and send it
			self.wfile.write(bytes(json.dumps(post), "utf-8"))


	def handleCreate(self):
		#f = open("file.txt", "a")
		#read the content-length header from the client (number in bytes)
		length = self.headers["Content-length"]

		#read the body data from the client
		body = self.rfile.read(int(length)).decode("utf-8") #recieve data from client
		#print("the body:",body) #body is firstname=dj&lastnaame=holt

		data = parse_qs(body) #parse query string(qs)
		#print("the data:", data)

		name = data['name'][0]
		age = data['age'][0]
		sentence = data['sentence'][0] #data works as a dictonary with a list of values.
		date = data['date'][0]
		ten = data['ten'][0]

		sentence = sentence.replace("\n", " ")
		
		db = dataDB()
		db.createfourm(name, age, sentence, date, ten)
		# paragraphs.append(sentence)
		self.send_response(201)
		self.send_header("Access-Control-Allow-Origin", "*")
		self.end_headers()
		#f.close()

	def handleNotFound(self):
		self.send_response(404) 
		self.send_header("Content-type", "text/html") 
		self.end_headers() 
		self.wfile.write(bytes("<h1>Not Found</h1>", "utf-8"))

	def handleList(self):
		#f=open("file.txt", "r")
		#paragraphs = []
		self.send_response(200) #sending a response hello(200).
		self.send_header("Content-type", "application/json") #put in headers. This is also a MIME type
		self.send_header("Access-Control-Allow-Origin", "*") #star means all orgins
		self.end_headers() #puts ribbon on the request and send it

		db = dataDB()
		fourm = db.getfourms()

		self.wfile.write(bytes(json.dumps(fourm), "utf-8")) #file we write to send data to client
		#json.dumps is dumping string of value
		#virtual file to recieve and buffer data need to be in
		#f.close()

def run():
	listen = ("0.0.0.0", 8080)
	server = HTTPServer(listen, MyHandler)
	print("Listening...")
	server.serve_forever()

run()