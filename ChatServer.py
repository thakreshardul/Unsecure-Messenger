import socket
import argparse
import select
# Displays help message and the usage
parser = argparse.ArgumentParser(description='Starts a UDP chat server')
parser.add_argument('-sp', '--server-port', required=True, type=int,
                    metavar='Server_port', help='server port number')
args = parser.parse_args()

HOST = '127.0.0.1' # start the server on localhost
PORT = args.server_port # port form the command line argument

clients = [] # Stores the client information

# Initialize the server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((HOST,PORT))
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.setblocking(0)  # Non blocking
print "CHAT SERVER HAS BEEN STARTED ON %d" % PORT



quitting = False  # A flag that enables a user to Shut down the server

while not quitting:
    try:
        data_available = select.select([serverSocket], [], [])
        if data_available[0]:
            message, address = serverSocket.recvfrom(2048)
        if "Server-shutdown" in str(message):
            quitting = True
        if address not in clients and \
                        message == "Hello Server":  # Greeting message from client
            for client in clients:
                welcome_message = "Client" + str(address) + "joined"
                serverSocket.sendto(welcome_message, client)
            clients.append(address)
            serverSocket.sendto("Welcome to the Network Security chat room\n",
                                address)
            print "Client" + str(address) + "joined"
        else:
            new_message = "<From " + str(address) + ">" + str(message)
            for client in clients:
                serverSocket.sendto(new_message, client)
            print new_message
    except Exception as e:
        print e  # Catches all exceptions
        serverSocket.close()
        break

serverSocket.close()