import socket
import threading
import argparse
import select

# Displays help message and the usage
parser = argparse.ArgumentParser(description='Starts a chat client')
parser.add_argument('-sip', '--server-ip-address', required=True,
                    metavar='Server_IP_Address', help='Server IP address')
parser.add_argument('-sp', '--server-port', type=int, required=True,
                    metavar='Server_Port', help='Server port number')
parser.add_argument('-cp', '--client-port', type=int, required=True,
                    metavar='Client_Port', help='Client port number')
args = parser.parse_args()

HOST = '127.0.0.1' # Starts the server on localhost
PORT = args.client_port # Client port from the command line argument
# A tuple tht stores server's ip and port
SERVER = (str(args.server_ip_address), args.server_port)

threadRLock = threading.RLock() # A thread reentrant lock for receive function
threadLock = threading.Lock() # A thread lock for writing

shutdown = False # A flag to shutdown client

# A function to process incoming messages
def receiving(name, sock):
    while not shutdown:
        try:
            data_available = select.select([clientSocket], [], [])
            threadLock.acquire()
            if data_available[0]:
                data, address = clientSocket.recvfrom(1024)
                print str(data)
        except Exception as e:
            print e
            break
        finally:
            threadLock.release()
# Initialise the server socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientSocket.bind((HOST, PORT))
clientSocket.setblocking(0) # Non blocking

greeting_message = "Hello Server"
clientSocket.sendto(greeting_message, SERVER)

# Create a thread and start it for receiving incoming messages
receivingThread = threading.Thread(target=receiving, args=("RecvThread",clientSocket))
receivingThread.start()

message = raw_input("-> ")  # Get input from the user
while message != 'q':  # User exits by enter the character 'q'
    if message != '':
        clientSocket.sendto(message, SERVER)
    message = raw_input("-> ")
receivingThread.join()
clientSocket.close()