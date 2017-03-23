#!/usr/bin/env python

#!/usr/bin/env python

import socket


HOST = '10.26.1.65'
PORT = 23
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
s= None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        print 'first one did not work'
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
else:
    s.sendall('Once again, Hello, world \n')
    i=0
    while i < 100:
        data = s.recv(1024)
        i += 1
        print('Received', repr(data))

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'finished this ok 1'
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data

'''
