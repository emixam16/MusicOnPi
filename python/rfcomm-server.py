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

class Downloader(Thread):
	def __init__(self, id_mus):
		Thread.__init__(self)
		self.id_mus = id_mus
	def run(self):
		subprocess.call(['youtube-dl',self.id_mus,'-x','-o','../sound/%(id)s.%(ext)s'])
		fifo_music.put(self.id_mus);


class FIFODownloader(Thread):
	def __init__(self, fifo):
		Thread.__init__(self)
		self.fifo = fifo
	def run(self):
		id_mus = self.fifo.get()
		while(id_mus != ''):
			subprocess.call(['youtube-dl',id_mus,'-x','-o','../sound/%(id)s.%(ext)s'])
			fifo_music.put(id_mus);
			id_mus=self.fifo.get()

class Reader(Thread):
	def __init__(self, id_mus):
		Thread.__init__(self)
		self.id_mus = id_mus
	def run(self):
		subprocess.call("mpv "+self.id_mus+".*",shell=True)

class FIFOReader(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		id_mus = fifo_music.get()
		while(id_mus != ''):
			subprocess.call("mpv --input-file=/../config/mpvinput"+id_mus+".*",shell=True)
			id_mus=fifo_music.get()
		

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
print 'before'
advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
                   protocols = [ OBEX_UUID ] 
                    )
                   
print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info

pool = ThreadPool(processes=2)

data_out=''

fifo_music = Queue.Queue()

try:
	while True:
		data = client_sock.recv(1024)
		if len(data) == 0:
			break
		print "received [%s]" % data	
		if data == 'Reponds':
			data_out = 'Reponse !'
		elif data == 'PLAY':
			subprocess.call(['mpv',id_musique+'.mp3'])
			data_out = 'playing'
		elif data == 'PAUSE':
			data_out = 'notplaying'
			thread2.join()
		else:
			#TODO change path...
			x=subprocess.Popen(["php","start.php", data],stdout=subprocess.PIPE, stderr=subprocess.PIPE)      
			#print "code retour: ",x.wait()
			#print "sortie erreur"
			#print x.stderr.read()
			#print "sortie standard"

			output = x.stdout.read()
			# print output
			output = json.loads(output)
			fifo_download = Queue.Queue()

			for i in range(10):
				fifo_download.put(output[i]['id'])

				id_musique = output[0]['id'] 
				#subprocess.call(['youtube-dl',id_musique,'-x','-o','%(id)s.%(ext)s'])
				#subprocess.call(['youtube-dl',id_musique,'-x','--audio-format','mp3','-o','%(id)s.%(ext)s'])

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
