#need to change this PROJECT1 RS to Load-Balancing Server
#DOES NOT store mappings from hostnames to IP addresses
#1st

#must add these python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort
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
#not sure yet if we need to remove any parsers that have action=store
CurrentHOST = ''
parser = argparse.ArgumentParser(description="""lsListen Port""")
parser = argparse.ArgumentParser(description="""TS1HostName Port""")
parser = argparse.ArgumentParser(description="""TS1Listen Port""")
parser = argparse.ArgumentParser(description="""TS2HostName Port""")
parser = argparse.ArgumentParser(description="""TS2Listen Port""")
parser.add_argument('rsListenPort', type=int, action='store')
parser.add_argument('-f', type=str, default='PROJI-DNSRS.txt', action='store', dest='in_file')

args = parser.parse_args(argv[1:])
rsListenPort = args.rsListenPort
# form key values for in_file using Hashmap


# use socket() function to start socket protocal
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # FOR LOCAL CLIENT HANDLING

# bind the server.py to client.py
serverSock.bind((CurrentHOST, rsListenPort))

# after binding, listen to client
serverSock.listen(1)
newSock, serverAddress = serverSock.accept()

table = {}
with open('PROJI-DNSRS.txt', 'r') as file:
    for line in file:
        host, ipAddress, flag = line.strip().split(' ')
        if "NS" == flag:
            tsServerName=host
        else:
            table[host] = ipAddress, flag
newSock.send(tsServerName.encode('utf-8'))
# while the server is listening it checks then decodes messages

while True:

    txtReceived = newSock.recv(512)
    txt = txtReceived.decode('utf-8').lower()

    if not txtReceived:

        break
    if txt in table:
        text = table.get(txt)
        untuplemessage = " "+ text[0] +" " + text[1]
        newSock.send(untuplemessage.encode('utf-8'))
    else:
        newSock.send("NS".encode('utf-8'))

# close socket
newSock.close()
exit()
