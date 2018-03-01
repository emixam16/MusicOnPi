msg ="azerty"
key = open("key.txt", "r").read()
offFile = open("offset", "r")
offset = int(offFile.read())
i=0
out = [None] * len(msg)
while(i < len(msg)):
	out[i] = chr(ord(msg[i]) ^ ord(key[offset]))
	offset = (offset+1) % len(key)
	i+=1
offFile.close()
offFile = open("offset", "w");
offFile.write(str(offset))
print out
