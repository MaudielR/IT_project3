# need to change this PROJECT1 RS to Load-Balancing Server
# DOES NOT store mappings from hostnames to IP addresses
# 1st

# must add these python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort
# then make sure that Client recieves messages from here
# then make sure connection between here, client, ts1 and ts2 is stable
# 2nd

# Use hash table to store and divide queries evenly
# 3rd
# make sure that if one of the servers crashes (or is closed)
# in the middle, the LS server continues to answer queries using only the
# other server.
import socket
import sys
# need to change this PROJECT1 RS to Load-Balancing Server
# 1st


# then make sure that Client recieves messages from here
# then make sure connection between here, client, ts1 and ts2 is stable
# 2nd

# Use hash table to store and divide queries evenly
# 3rd
# make sure that if one of the servers crashes (or is closed)
# in the middle, the LS server continues to answer queries using only the
# other server.
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

# arrays to hold the previous requests to be able to send it to the same place every time.
ts1Table = []
ts2Table = []

# while the server is listening it checks then decodes messages
while True:
    # Get host name from client
    request = clientSock.recv(512)
    clientRequestedName = request.decode('utf-8').lower()
    #TA Abraham lecture

    newmessege =hashlib.sha224(clientRequestedName.encode('utf-8')).digest()[0]
    # if client stops sending then stop trying to send anything
    if not request:
        break

    # If it's client is still sending requests then do the following things...
    else:

        # If the request has gone to ts1 in the past, send it there again...
        if newmessege % 2 == 0:
            try:
                print('sending to ts1')
                ts1ServerSock.sendall(request)
                answer = ts1ServerSock.recv(512)
                print(answer.decode('UTF-8'))
                if(answer.decode('UTF-8')=='error'):
                    try:
                        print('sending to ts2')
                        ts2ServerSock.sendall(request)
                        answer = ts2ServerSock.recv(512)
                        print(answer.decode('UTF-8'))
                        
                        if(answer.decode('UTF-8')=='error'):
                            clientSock.sendall(answer)
                        else:
                            clientSock.sendall(answer)
                            continue
                    except:
                        print('both ts1 and ts2 failed')
                        clientSock.sendall(answer)
                        continue
                else:
                    clientSock.sendall(answer)
            except:
                #this is where there was an error connecting to one of the servers
                clientSock.sendall('')
                continue

        # If the request has gone to ts2 in the past, send it there again...
        elif newmessege%2 != 0:
            try:
                print('sending to ts2')
                ts2ServerSock.sendall(request)
                answer = ts2ServerSock.recv(512)
                print(answer.decode('UTF-8'))
                if(answer.decode('UTF-8')=='error'):
                    try:
                        print('sending to ts1')
                        ts1ServerSock.sendall(request)
                        answer = ts1ServerSock.recv(512) 
                        print(answer.decode('UTF-8'))
                        
                        if(answer.decode('UTF-8')=='error'):
                            clientSock.sendall(answer)
                        else:
                            clientSock.sendall(answer)
                            continue
                    except:
                        clientSock.sendall(answer)
                        print('both ts2 and ts1 failed')
                        continue
                else:
                    clientSock.sendall(answer)
            except:
                #this is if there was an error with connecting to one of the servers
                clientSock.sendall('')
                continue
                    
            

        # If it hasn't gone to either than send it to the one who has had less requests to balance the load

        # send to ts1 if that has had less...
        # elif ts1Table.len < ts2Table.len:
        #     ts1Table.append(clientRequestedName)
        #     ts1ServerSock.sendall(clientRequestedName.edncode('utf-8'))
        #     answer = ts1ServerSock.recv(512)  # might need more depending on size
        #     clientSock.sendall(answer)
        #
        # # send to ts2 if that has had less or equal amount of requests....
        # else:
        #     ts2Table.append(clientRequestedName)
        #     ts2ServerSock.sendall(clientRequestedName.edncode('utf-8'))
        #     answer = ts2ServerSock.recv(512)  # might need more depending on size
        #     clientSock.sendall(answer)

# close sockets
clientSock.close()
ts1ServerSock.close()
ts2ServerSock.close()
exit()
