#need to change this PROJECT1 RS to Load-Balancing Server
#1st


#then make sure that Client recieves messages from here
#then make sure connection between here, client, ts1 and ts2 is stable
#2nd

#Use hash table to store and divide queries evenly
#3rd
#make sure that if one of the servers crashes (or is closed)
#in the middle, the LS server continues to answer queries using only the
# other server.
import socket
import sys
import argparse
from sys import argv
import binascii
import struct
import hashlib
#must add these python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort
CurrentHOST = ''



parser = argparse.ArgumentParser(description="""ls""")
parser.add_argument('lsListenPort', type=int, action='store')
parser.add_argument('ts1HostName', type=str, action='store')
parser.add_argument('ts1ListenPort', type=int, action='store')
parser.add_argument('ts2HostName', type=str, action='store')
parser.add_argument('ts2ListenPort', type=int, action='store')

args = parser.parse_args(argv[1:])
lsListenPort = args.lsListenPort
ts1ListenPort= args.ts1ListenPort
ts2ListenPort= args.ts2ListenPort
# form key values for in_file using Hashmap


# use socket() function to start socket protocal
lsServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # FOR LOCAL CLIENT HANDLING

# bind the server.py to client.py
lsServerSock.bind((CurrentHOST, lsListenPort))


# after binding, listen to client
lsServerSock.listen(1)
clientSock, serverAddress = lsServerSock.accept()

lsServerSock.connect((args.ts1HostName, ts1ListenPort))
lsServerSock.connect((args.ts2HostName, ts2ListenPort))
ts1Table = []
ts2Table = []
#clientSock.send(tsServerName.encode('utf-8'))
# while the server is listening it checks then decodes messages

while True:

    txtReceived = clientSock.recv(512)
    txt = txtReceived.decode('utf-8').lower()

    if not txtReceived:

        break
    else:
        text = "hello"
        untuplemessage = " "+ text[0] +" " + text[1]
        clientSock.send(untuplemessage.encode('utf-8'))


# close socket
clientSock.close()
exit()
