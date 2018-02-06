#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import json
import subprocess
from .threads import *
from youtube_dl import YoutubeDL

class CommandManager(object):
	def answerCommand(self, params, user, source):
		# Used to check that the script is still running
		return "Reponse!"

	def playCommand(self, params, user, source):
		subprocess.call(['mpv',id_musique+'.mp3'])
		return 'playing'

	def pauseCommand(self, params, user, source):
		if user.context.song_thread is not None:
			user.context.song_thread.join()
		return 'notplaying'

	def searchCommand(self, params, user, source):
		x=subprocess.Popen(["php","../php/start.php", ' '.join(params[1:])],stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		try:
			output = x.stdout.read()
			print(output)
			output = json.loads(output)
			fifo_download = user.context.pending_downloads
			print("Search start")

			for i in range(10):
				fifo_download.put(output[i]['id'])
		except Exception as e:
			return(str(e))

		print("Search start")
		id_musique = output[0]['id']
		#subprocess.call(['youtube-dl',id_musique,'-x','-o','%(id)s.%(ext)s'])
		#subprocess.call(['youtube-dl',id_musique,'-x','--audio-format','mp3','-o','%(id)s.%(ext)s'])

		thread1 = Downloader(fifo_download.get())
		thread1.start()
		thread1.join()

		thread2=FIFOReader(user.context.pending_songs)
		thread2.start()
		user.context.song_thread = thread2
		data_out="playing"

		thread3=FIFODownloader(fifo_download)
		thread3.start()
		return "Started playing"

	def authCommand(self, params, user, source):
		login = params[0]
		hashe = params[2]
		#login_dur_temp='deni'
		#mdp_dur_temp='ah'
		found=False
		dummy=False
		with open("./passwords","r") as F:
			for line in F:
				if login+' ' in line:
					hashe_dur_temp = line.split(' ')[1]
					found=True
					break
		if found:
			#h1 = sha256()
			#h1.update(mdp_dur_temp)
			#hashe_dur_temp = h1.hexdigest().upper()
			print ("hash recu : ", hashe)
			print ("hash calcule : ", hashe_dur_temp)
			print (hashe == hashe_dur_temp)
			if hashe == hashe_dur_temp:
				authentifie=params[0]
				data_out = "connected!"
				#client_sock.send(data_out)
			else:
				print ("auth failed:bad password")
				data_out = "notconnected!"
				#client_sock.send(data_out)
		else:
			print ("auth failed:login not found")
			data_out = "notconnected!"
			#client_sock.send(data_out)
		return data_out

	def signCommand(self, params, user, source):
		found=False
		with open("./passwords","r") as F:
			for line in F:
				if params[0]+' ' in line:
					found=True
					break
		if not(found):
			with open("./passwords","a") as F:
				F.write(params[0] + ' ' + params[2]+" \n")
			authentifie=params[0]
			data_out = "registered!"

			#client_sock.send(data_out)
		else:
			print ("already signed")
			data_out = "already exists!"
			#client_sock.send(data_out)
		return data_out

	def decoCommand(self, params, user, source):
		user.disconnect(source)

	def run(self, command, params, user, source):
		if(len(command) <= 0):
			return
		command_name = command.lower() + "Command"
		if(hasattr(self, command_name)):
			return getattr(self, command_name)(params, user, source)
		else:
			return "No such command"

if __name__ == "__main__":
	print("Command manager")

