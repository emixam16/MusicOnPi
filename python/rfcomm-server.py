#!/bin/python
# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import subprocess
import json
from threading import Thread
from multiprocessing.pool import ThreadPool
import Queue
from hashlib import sha256

class Downloader(Thread):
	def __init__(self, id_mus):
		Thread.__init__(self)
		self.id_mus = id_mus
	def run(self):
		subprocess.call(['youtube-dl',self.id_mus,'-x','-o',"~/MusicOnPi/sound/%(id)s.%(ext)s"])
		fifo_music.put(self.id_mus);


class FIFODownloader(Thread):
	def __init__(self, fifo):
		Thread.__init__(self)
		self.fifo = fifo
	def run(self):
		id_mus = self.fifo.get()
		while(id_mus != ''):
			subprocess.call(['youtube-dl',id_mus,'-x','-o',"~/MusicOnPi/sound/%(id)s.%(ext)s"])
			fifo_music.put(id_mus);
			id_mus=self.fifo.get()

class Reader(Thread):
	def __init__(self, id_mus):
		Thread.__init__(self)
		self.id_mus = id_mus
	def run(self):
		subprocess.call("mpv ~/MusicOnPi/sound/"+self.id_mus+".* --input-fil=~/MusicOnPi/config/mpvInput",shell=True)

class FIFOReader(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		id_mus = fifo_music.get()
		while(id_mus != ''):
			subprocess.call("mpv ~/MusicOnPi/sound/"+id_mus+".* --input-file=~/MusicOnPi/config/mpvInput",shell=True)
			id_mus=fifo_music.get()


server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

print("Lancement du client serveur")
#advertise_service( server_sock, "SampleServer",
#			service_id = uuid,
#			service_classes = [ uuid, SERIAL_PORT_CLASS ],
#			profiles = [ SERIAL_PORT_PROFILE ],
#			protocols = [ OBEX_UUID ]
#			)

print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

pool = ThreadPool(processes=2)

data_out=''

fifo_music = Queue.Queue()

authentifie=' '

try:
	while True:
		datas = client_sock.recv(1024)
		if len(datas) == 0:
			break
		print "received [%s]" % datas
		data = datas.split(' ')

		if (data[1] == 'auth' and len(data) == 3):
			login = data[0]
			hashe = data[2]
			#login_dur_temp='deni'
			#mdp_dur_temp='ah'
			found=False
			F = open("./passwords","r")
			for line in F:
				if login+' ' in line:
					hashe_dur_temp = line.split(' ')[1]
					found=True
					break
			if found:
				#h1 = sha256()
				#h1.update(mdp_dur_temp)
				#hashe_dur_temp = h1.hexdigest().upper()
				print "hash recu",hashe
				print "hash calcule",hashe_dur_temp
				print hashe == hashe_dur_temp
				if hashe == hashe_dur_temp:
					authentifie=data[0]
					data_out = "connected!"
					#client_sock.send(data_out)
				else:
					print "auth failed:bad password"
					data_out = "notconnected!"
					#client_sock.send(data_out)
			else:
				print "auth failed:login not found"
				data_out = "notconnected!"
				#client_sock.send(data_out)

			F.close()

		elif (data[1] == 'sign' and len(data) == 3):
			found=False
			F = open("./passwords","r")
			for line in F:
				if data[0]+' ' in line:
					found=True
					break
			F.close()
			if not(found):
				F = open("./passwords","a")
				F.write(data[0] + ' ' + data[2]+" \n")
				authentifie=data[0]
				F.close()
				data_out = "registered!"
				#client_sock.send(data_out)

			else:
				print "already signed"
				data_out = "already exists!"
				#client_sock.send(data_out)


		elif data[1] == 'deco':
			authentifie= ' '

		if authentifie != data[0]:
			print "Authentication failed"


		elif data[1] == 'Reponds':
				data_out = 'Reponse!'

		elif data[1] == 'play':
			subprocess.call("php ~/MusicOnPi/php/start.php pause",shell=True)
                elif data[1] == 'volume':
                        print "php ~/MusicOnPi/php/start.php volume "+data[2]
                        subprocess.call("php ~/MusicOnPi/php/start.php 'volume "+data[2]+'\'',shell=True)
#data_out = 'playing'
#		elif data[1] == 'PAUSE':
#			data_out = 'notplaying'
#			thread2.join()
		elif data[1] == 'search':
			#TODO change path...
			data2 = data[1]
			i=2
			while i < len(data):
				data2 = data2 + ' ' + data[i]
				i=i+1
			print data2
			x=subprocess.Popen(["php","../php/start.php", data2],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#print "code retour: ",x.wait()
			#print "sortie erreur"
			#print x.stderr.read()
			#print "sortie standard"

			output = x.stdout.read()
			print output
			output = json.loads(output)
			fifo_download = Queue.Queue()

			for i in range(10):
				fifo_download.put(output[i]['id'])

			id_musique = output[0]['id']

			thread1 = Downloader(fifo_download.get())
			thread1.start()
			thread1.join()

			thread2=FIFOReader()
			thread2.start()
			data_out="playing"

			thread3=FIFODownloader(fifo_download)
			thread3.start()

		client_sock.send(data_out)

except IOError:
	pass

print "disconnected"

client_sock.close()
server_sock.close()
print "all done"

