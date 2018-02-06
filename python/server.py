#!/usr/bin/env python2
# encoding: utf-8

from MusicOnPi import CommandManager
from MusicOnPi.config.globalcontext import GlobalContext
from MusicOnPi.user import DisconnectedUser
from select import select
import sys
import subprocess

if __name__ == "__main__":
	accept_bridges=[]
	print("Starting...")
	if len(sys.argv)<=1 or sys.argv[1] in ['bluetooth', 'hybrid']:
		# Detect if service advertising is going to cause a shutdown on current raspberry
		would_shutdown = subprocess.call(['python', 'advertise_test.py']) != 0

		# Set-up bluetooth server
		import bluetooth
		server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		server_sock.bind(("", bluetooth.PORT_ANY))
		server_sock.listen(1)
		accept_bridges.append(server_sock)
		print("Waiting for bluetooth connection on RFCOMM channel %d".format(server_sock.getsockname()[1]))
		# Service advertisement
		# TODO: find out why it doesn't work on all PIs
		if not would_shutdown:
			uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
			#bluetooth.advertise_service( server_sock, "SampleServer",
			#	service_id = uuid,
			#	service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
			#	profiles = [ bluetooth.SERIAL_PORT_PROFILE ],
			#	protocols = [ bluetooth.OBEX_UUID ]
			#	)

	if len(sys.argv)>1 and sys.argv[1] in ['web', 'hybrid']:
		# Set-up web server
		# Only use for debug
		import socket
		server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_sock.bind(("", 8888))
		server_sock.listen(5)
		accept_bridges.append(server_sock)
		print("Waiting for network connection on port 8888")

	if len(accept_bridges) == 0:
		# if no proper option was received
		print("Please choose 'bluetooth', 'web' or 'hybrid' as mode")
		exit(1)

	manager = CommandManager()
	socket_list = accept_bridges[:]

	while True:
		# Main loop
		readable_list= select(socket_list, [], [])[0]
		try:
			for socket in readable_list:
				if socket in accept_bridges:
					# Manage new connection
					csock, cinfo = socket.accept()
					csock.setblocking(0)
					print ("Accepted connection from ", cinfo, csock)
					socket_list.append(csock)
					continue
				try:
					data = socket.recv(1024)
				except Exception as e:
					# One-sided disconnect
					socket_list.remove(socket)
					socket.close()
					continue
					
				if len(data) == 0:
					# Close dead connection
					socket_list.remove(socket)
					socket.close()
					continue

				# Find the user associated with the socket if he exists
				current_user = None
				for u in GlobalContext.user_list:
					if u.hasSocket(socket):
						current_user = u
						break
				if current_user is None:
					current_user = DisconnectedUser()

				# Perform requested action
				print("Received : '", data, "' from ", socket)
				data = data.split(' ')
				try:
					answer = manager.run(data[1], data, current_user, socket)
					if answer and len(answer) > 0:
						socket.send(answer)
				except Exception as e:
					print(e)
		except Exception as e:
			print("Unhandled exception ", e)
			print("Please let the devs know")

