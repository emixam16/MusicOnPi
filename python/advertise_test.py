#!/usr/bin/env python2
#encoding=utf-8

from bluetooth import *
import sys

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(4)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

print("Lancement du client serveur")
advertise_service( server_sock, "SampleServer",
			service_id = uuid,
			service_classes = [ uuid, SERIAL_PORT_CLASS ],
			profiles = [ SERIAL_PORT_PROFILE ],
			protocols = [ OBEX_UUID ]
			)

sys.exit(0)
