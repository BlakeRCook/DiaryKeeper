import os, base64
class SessionStore:

	def __init__(self):
		#this is your file cabinet
		#will contain many dictionarys
		#one per session
		self.sessions = {}
		return

	def generateSessionId(self):
		rnum = os.urandom(32)
		rstr = base64.b64encode(rnum).decode("utf-8")
		return rstr

	def createSession(self):
		sessionId = self.generateSessionId()
		#add a new seession (dictinary) to the file cabinet
		#use new generated sessino id
		self.sessions[sessionId] = {}
		return sessionId

	def getSession(self, sessionId):
		if sessionId in self.sessions:
			#retrun existing session by Id
			return self.sessions[sessionId]
		else:
			#return nonthing if id is invalid
			return None