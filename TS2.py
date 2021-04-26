#must change this to cloudflare (1.1.1.1)
#double check if clouflare port is 80
import argparse
import binascii
import socket
from sys import argv
import struct

#temp host holder
Host = ''
#get the port from aguments given
parser = argparse.ArgumentParser(description="""This is a Server program""")
parser.add_argument('port', type=int, help='this is the port to connect to the server on', action='store')
args = parser.parse_args(argv[1:])
port= args.port

#try and create socket to connect to google DNS server
try:
    cloudflare_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

#connect to google DNS server
cloudflare_addr = ('1.1.1.1', 80)
cloudflare_sock.connect(cloudflare_addr)


#try and create socket to connect to client
try:
    server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.err as err:
    print('socket open error: {} \n'.format(err))

#listen and connect to the client trying to connect
server_sock.bind(('',port))
server_sock.listen(1)
newSock, serverAddress = server_sock.accept()


#decode the message and then send as UDP packet to google DNS server
def message_generator(url):

    split_url = url.split('.')
    answer = ""

    for section in split_url:
        answer_len = len(section)
        if len(section) < 10:
            answer_len = '0' + str(len(section))
        answer = answer + answer_len + ""
        for character in section:
            hexcode = format(ord(character), "x")
            hexcode = hexcode.upper()
            answer = answer +hexcode + ""


    answer = answer + "0000010001"
    message = "AAAA01000001000000000000" + answer
    return message

def newans(newData):
    holder= ''
    pt = newData
    fin = [pt[i:i+32] for i in range(0, len(pt), 32)]

    #might do a check for A type message here
    for section in fin:
        section = section[-8:]
        final = [section[i:i+2] for i in range(0, len(section), 2)]
        ans = ""
        for x in final:
            x = str(int(x, 16)) + '.'
            ans = ans + x + ''
        newans = ans[:-1]
        holder = holder + ' '+newans + ' '+ ','
    holder = holder[:-1]
    #print(newans)
    return holder


#first while the client and google is connected
def send_message(message):
    #send send answer back to client (if multiple separate by ',') if none send 'OTHER'
    newSock.sendall(message.encode('utf-8'))
    pass


while True:
    #retrieve the message (host name) from client
    client_message = newSock.recv(256).decode('utf-8')
    if(len(client_message) == 0):
        break

    dnsMessage = message_generator(client_message)

    #from https://routley.io/posts/hand-writing-dns-messages/
    google_sock.sendto(binascii.unhexlify(dnsMessage), google_addr)

    #then retrieve the answer from google DNS server and decode
    #from https://routley.io/posts/hand-writing-dns-messages/
    udpOnlineData, addr = google_sock.recvfrom(4096)

    respond = binascii.hexlify(udpOnlineData).decode('utf-8')
    print('responce',respond)

    length = len(dnsMessage)
    respond=respond[length:]
    print('responce',respond)
    #check the type of response we are receiving
    ipv4_size=respond[4:8]
    if ipv4_size != '0001':
        message_length = respond[22:24]

        #use the size of the message that is NOT type 'A' to remove it from the full response
        message_length = (int(message_length, 16)* 2)+24
        message = respond[message_length:]
        message =newans(message)
        message = ' other,' + message
        send_message(message)
    else:
        message = newans(respond)
        send_message((message))

#disconnect from client and google DNS
server_sock.close()
exit()

