from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
import datetime

# paragraphs = []
class MyHandler (BaseHTTPRequestHandler):
	def do_GET(self):
		print("Path:", self.path)
		if self.path == "/messages": #path for the request
			self.handleList()
		else: 
			self.handleNotFound() 

	def do_POST(self):
		if self.path == "/messages":
			f = open("file.txt", "a")
			#read the content-length header from the client (number in bytes)
			length = self.headers["Content-length"]
			#read the body data from the client
			body = self.rfile.read(int(length)).decode("utf-8") #recieve data from client
			print("the body:",body) #body is firstname=dj&lastnaame=holt
			data = parse_qs(body) #parse query string(qs)
			print("the data:", data)

			sentence = data['sentence'][0] #data works as a dictonary with a list of values.
			print("sentence",sentence)
			sentence = sentence.replace("\n", " ")
			date = datetime.datetime.now()
			f.write(date.strftime("%Y-%m-%d %H:%M") + ":  " + sentence + "\r\n");
			print("the sentence was writen to file")
			# paragraphs.append(sentence)

			self.send_response(201)
			self.send_header("Access-Control-Allow-Origin", "*")
			self.end_headers()
			f.close()
		else:
			self.handleNotFound()
			
		

	def handleNotFound(self):
		self.send_response(404) 
		self.send_header("Content-type", "text/html") 
		self.end_headers() 
		self.wfile.write(bytes("<h1>Not Found</h1>", "utf-8"))

	def handleList(self):
		f=open("file.txt", "r")
		paragraphs = []
		self.send_response(200) #sending a response hello(200).
		self.send_header("Content-type", "application/json") #put in headers. This is also a MIME type
		self.send_header("Access-Control-Allow-Origin", "*") #star means all orgins
		self.end_headers() #puts ribbon on the request and send it
		contents = f.readlines()
		for x in contents:
			if x == "\n" or x =="\r":
				#do nothing
				pass
			else:
				paragraphs.append(x)
		self.wfile.write(bytes(json.dumps(paragraphs), "utf-8")) #file we write to send data to client
		#json.dumps is dumping string of value
		#virtual file to recieve and buffer data need to be in
		f.close()

def run():
	listen = ("0.0.0.0", 8080)
	server = HTTPServer(listen, MyHandler)
	print("Listening...")
	server.serve_forever()

run()