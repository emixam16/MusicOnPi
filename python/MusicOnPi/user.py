#!/usr/bin/env python
# encoding: utf-8

from .config.globalcontext import GlobalContext

__all__ = [
		'User',
	]

class User(object):
	def __init__(self, name):
		self.name = name
		self.authenticated = True
		self.sockets = []

	def getName(self, default="Not Connected"):
		return self.name if self.authenticated else default

	def add_connection(self, socket):
		self.sock_list.append(socket)

	def revoke_connection(self, socket):
		pass

	def disconnect(self):
		self.authenticated = False

	def hasSocket(self, socket):
		for s in self.sockets:
			if s == socket:
				return True
		return False

	@property
	def get_context(self):
		return GlobalContext

class DisconnectedUser(User):
	def __init__(self):
		User.__init__(self, "")
		self.authenticated = False

if __name__ == "__main__":
	print("This file provides a User object used to authenticate a connection.")
