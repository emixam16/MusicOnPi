#!/usr/bin/env
#encoding: utf-8

import Queue

class GlobalContext(object):
	song_list=[] # Not used
	pending_downloads=Queue.Queue()
	pending_songs=Queue.Queue() # Used to play songs
	config_state={} # not used
	user_list=[]
	song_thread=None

	def __init__(self):
		raise Exception("Do not instanciate this class")

if __name__ == '__main__':
	print("Global context, yo")
