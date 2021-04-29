import socket
import sys
import argparse
from sys import argv
import binascii
import struct
import hashlib

parser = argparse.ArgumentParser(description="""ls""")
parser.add_argument('lsListenPort', type=int, action='store')
parser.add_argument('ts1HostName', type=str, action='store')
parser.add_argument('ts1ListenPort', type=int, action='store')
parser.add_argument('ts2HostName', type=str, action='store')
parser.add_argument('ts2ListenPort', type=int, action='store')
args = parser.parse_args(argv[1:])

# use socket() function to start socket protocal
lsServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts1ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts2ServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind and listen to conenct server.py to client.py
lsServerSock.bind(('', args.lsListenPort))
lsServerSock.listen(1)
clientSock, serverAddress = lsServerSock.accept()

# try and connect to the ts servers at the given addresses
ts1ServerSock.connect((args.ts1HostName, args.ts1ListenPort))
ts2ServerSock.connect((args.ts2HostName, args.ts2ListenPort))

# while the server is listening it checks then decodes messages
while True:
    # Get host name from client
    request = clientSock.recv(512)
    clientRequestedName = request.decode('utf-8').lower()

    # TA Abraham lecture, showed us how to use hashlib.sha224
    newmessege = hashlib.sha224(clientRequestedName.encode('utf-8')).digest()[0]
    # if client stops sending then stop trying to send anything
    if not request:
        break

    # If it's client is still sending requests then do the following things...
    else:

        # If the request has gone to ts1 in the past, send it there again...
        if newmessege % 2 == 0:
            try:
                ts1ServerSock.sendall(request)
                answer = ts1ServerSock.recv(512)
                if ((answer.decode('UTF-8') == 'error') or (answer.decode('UTF-8') == '')):
                    try:

                        ts2ServerSock.sendall(request)
                        answer = ts2ServerSock.recv(512)

                        if ((answer.decode('UTF-8') == 'error') or (answer.decode('UTF-8') == '')):
                            answer = ' - Error:HOST NOT FOUND'
                            answer = request + answer.encode('utf-8')
                            clientSock.sendall(answer)
                        else:
                            clientSock.sendall(answer)
                            continue
                    except:
                        answer = ' - Error:HOST NOT FOUND'
                        answer = request + answer.encode('utf-8')
                        clientSock.sendall(answer)
                        continue
                else:
                    clientSock.sendall(answer)
            except:
                # this is where there was an error connecting to one of the servers
                answer = ' - Error:HOST NOT FOUND'
                answer = request + answer.encode('utf-8')
                clientSock.sendall(answer)
                continue

        # If the request has gone to ts2 in the past, send it there again...
        elif newmessege % 2 != 0:
            try:
                ts2ServerSock.sendall(request)
                answer = ts2ServerSock.recv(512)
                if ((answer.decode('UTF-8') == 'error') or (answer.decode('UTF-8') == '')):
                    try:
                        ts1ServerSock.sendall(request)
                        answer = ts1ServerSock.recv(512)
                        if ((answer.decode('UTF-8') == 'error') or (answer.decode('UTF-8') == '')):
                            answer = ' - Error:HOST NOT FOUND'
                            answer = request + answer.encode('utf-8')
                            clientSock.sendall(answer)
                        else:
                            clientSock.sendall(answer)
                            continue
                    except:
                        answer = ' - Error:HOST NOT FOUND'
                        answer = request + answer.encode('utf-8')
                        clientSock.sendall(answer)
                        continue
                else:
                    clientSock.sendall(answer)
            except:
                # this is if there was an error with connecting to one of the servers
                answer = ' - Error:HOST NOT FOUND'
                answer = request + answer.encode('utf-8')
                clientSock.sendall(answer)
                continue

# close sockets
clientSock.close()
ts1ServerSock.close()
ts2ServerSock.close()
exit()
