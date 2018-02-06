
import subprocess
from threading import Thread
import youtube_dl

__all__ = ['Downloader',
		'FIFODownloader',
		'Reader',
		'FIFOReader',
		]

# TODO: use youtube_dl as a package instead of a process
class Downloader(Thread):
	def __init__(self, id_mus):
		Thread.__init__(self)
		self.id_mus = id_mus

	def run(self):
		subprocess.call(['youtube-dl',self.id_mus,'-x','-o','%(id)s.%(ext)s'])
		fifo_music.put(self.id_mus);

class FIFODownloader(Thread):
	def __init__(self, fifo):
		Thread.__init__(self)
		self.fifo = fifo

	def run(self):
		id_mus = self.fifo.get()
		while(id_mus != ''):
			subprocess.call(['youtube-dl',id_mus,'-x','-o','%(id)s.%(ext)s'])
			fifo_music.put(id_mus);
			id_mus=self.fifo.get()

class Reader(Thread):
	def __init__(self, id_mus):
		Thread.__init__(self)
		self.id_mus = id_mus

	def run(self):
		subprocess.call("mpv "+self.id_mus+".*",shell=True)

class FIFOReader(Thread):
	def __init__(self, fifo):
		Thread.__init__(self)
		self.fifo = fifo

	def run(self):
		id_mus = self.fifo.get()
		while(id_mus != ''):
			subprocess.call("mpv "+id_mus+".*",shell=True)
			id_mus=self.fifo.get()

