from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from data import dataDB
from data import UsersDB
import json
import datetime
from passlib.hash import bcrypt
from http import cookies
from SessionStore import SessionStore
from http import cookies
#from file import class

# paragraphs = []
gSessionStore = SessionStore()
class MyHandler (BaseHTTPRequestHandler):

	def load_cookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()

	def send_cookie(self):
		for morsel in self.cookie.values():
			self.send_header("Set-Cookie", morsel.OutputString())

	def load_session(self):
		#GOAL assign self.session according to sessionId
		self.load_cookie()
		if "sessionId" in self.cookie:
			sessionId = self.cookie["sessionId"].value
			self.session = gSessionStore.getSession(sessionId)
			if self.session == None:
				#session data does not exist for this id
				sessionId = gSessionStore.createSession()
				self.session = gSessionStore.getSession(sessionId)
				self.cookie["sessionId"] = sessionId
		else:
			#client has no session id yet.
			sessionId = gSessionStore.createSession()
			self.session = gSessionStore.getSession(sessionId)
			self.cookie["sessionId"] = sessionId
		print("CURRENT SESSION: ", self.session)
###################################################################################
	def do_OPTIONS(self):
		self.load_session()
		self.send_response(200)
		#self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		self.end_headers()
		return
	def do_GET(self):
		self.load_session()
		print("Path:", self.path)
		if self.path == "/messages": #path for the request
			self.handleList()
		elif self.path.startswith("/messages/"):
			parts = self.path.split("/")
			fourm_id = parts[2]
			self.handleFourmRetrieve(fourm_id)
		elif self.path == "/users":
			self.handleUsers()
		elif self.path == "/sessions":
			self.sessionretrieve()
		else: 
			self.handleNotFound() 

	def do_POST(self):
		self.load_session()
		if self.path == "/messages":
			self.handleCreate()
		elif self.path == "/users":
			self.UserCreate()
		elif self.path == "/sessions":
			self.StartSession()
		else:
			self.handleNotFound()
			
	def do_PUT(self):
		self.load_session()
		if self.path.startswith("/messages/"):
			parts = self.path.split("/")
			fourm_id = parts[2]
			self.handleFourmUpdate(fourm_id)
		else: 
			self.handleNotFound()

	def do_DELETE(self):
		self.load_session()
		if self.path.startswith("/messages/"):
			parts = self.path.split("/")
			fourm_id = parts[2]
			self.handleFourmDelete(fourm_id)
		else: 
			self.handleNotFound()


	def handleFourmDelete(self, fourm_id):
		if "userID" not in self.session:
			self.handle401()
			return

		db = dataDB()
		post = db.getfourm(fourm_id)

		if post == None:
			self.handleNotFound()
		else:
			db.deletefourm(fourm_id)
			self.send_response(200)
			self.end_headers() #puts ribbon on the request and send it

	def handleFourmUpdate(self, fourm_id):

		if "userID" not in self.session:
			self.handle401()
			return

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
			self.end_headers() #puts ribbon on the request and send it
			

	def handleFourmRetrieve(self, fourmID):
		if "userID" not in self.session:
			self.handle401()
			return

		db = dataDB()
		post = db.getfourm(fourmID)

		if post == None:
			self.handleNotFound()
		else:
			self.send_response(200)
			self.send_header("Content-type", "application/json") #put in headers. This is also a MIME type
			self.end_headers() #puts ribbon on the request and send it
			self.wfile.write(bytes(json.dumps(post), "utf-8"))


	def handleCreate(self):
		if "userID" not in self.session:
			self.handle401()
			return
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
		self.end_headers()
		#f.close()

	def handleNotFound(self):
		self.send_response(404) 
		self.send_header("Content-type", "text/html") 
		self.end_headers() 
		self.wfile.write(bytes("<h1>Not Found</h1>", "utf-8"))

	def handle401(self):
		self.send_response(401)
		self.send_header("Content-type", "text/html") 
		self.end_headers() 
		self.wfile.write(bytes("<h1>Error401</h1>", "utf-8"))

	def handleList(self):
		if "userID" not in self.session:
			self.handle401()
			return

		#f=open("file.txt", "r")
		#paragraphs = []
		self.send_response(200) #sending a response hello(200).
		self.send_header("Content-type", "application/json") #put in headers. This is also a MIME type
		self.end_headers() #puts ribbon on the request and send it

		db = dataDB()
		fourm = db.getfourms()

		self.wfile.write(bytes(json.dumps(fourm), "utf-8")) #file we write to send data to client
		#json.dumps is dumping string of value
		#virtual file to recieve and buffer data need to be in
		#f.close()

	def UserCreate(self):
		length = self.headers["Content-length"]

		body = self.rfile.read(int(length)).decode("utf-8") 

		data = parse_qs(body) 

		firstname = data['firstname'][0]
		lastname = data['lastname'][0]
		email = data['email'][0]
		password = data['password'][0]

		password = bcrypt.hash(password)
		#print("Email: ", email)
		#print("Password: ", password)
		userdb = UsersDB()
		user = userdb.getUserbyEmail(email)
		if user == None:
			userdb.createUser(firstname, lastname, email, password)
			self.send_response(201)
			self.end_headers()
		else:
			self.send_response(422)
			self.end_headers()
			

	def handleUsers(self):
		self.send_response(200) #sending a response hello(200).
		self.send_header("Content-type", "application/json") #put in headers. This is also a MIME type
		self.end_headers() #puts ribbon on the request and send it

		usersdb = UsersDB()
		listOfUsers = usersdb.getUsers()

		self.wfile.write(bytes(json.dumps(listOfUsers), "utf-8")) #file we write to send data to client

	def StartSession(self):
		length = self.headers["Content-length"]

		body = self.rfile.read(int(length)).decode("utf-8") 

		data = parse_qs(body) 

		email = data['email'][0]
		password = data['password'][0]

		userdb = UsersDB()
		user = userdb.getUserbyEmail(email)

		if user == None:
			self.handle401()
		else:
			if(bcrypt.verify(password, user['password'])):
				self.session["userID"] = user['id']
				self.send_response(200)
				self.end_headers()
			else:
				self.handle401()

	def end_headers(self):
		self.send_cookie()
		self.send_header("Access-Control-Allow-Origin", self.headers["Origin"]) #get rid of all allow origins in code
		self.send_header("Access-Control-Allow-Credentials", "true")
		BaseHTTPRequestHandler.end_headers(self)

	def sessionretrieve(self):
		if "userID" in self.session:
			userdb = UsersDB()
			user = userdb.getUser(self.session["userID"])
			self.send_response(200)
			self.send_header("Content-type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json.dumps(user), "utf-8"))
		else:
			self.handle401()


def run():
	listen = ("0.0.0.0", 8080)
	server = HTTPServer(listen, MyHandler)
	print("Listening...")
	server.serve_forever()

run()

# def sessionretrieve(self):
# 	if "userID" in self.session:
# 		db = pandadb()
# 		user = db.getuser(self.session["userid"])
# 		self.send_response(200)
# 		self.send_header("Content-type", "application/json")
# 		self.end_headers()
# 		self.wfile.write(bytes(json.dumps(user), "utf-8"))
# 	else:
# 		self.handle401()