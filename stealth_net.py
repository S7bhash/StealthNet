import sys
import socket
import threading
import pickle
import hashlib
from encryption import encrypt, decrypt


def server_loop():
	if len(sys.argv) == 1:
		print("[-] Please specify the proxy host and port...!")
		print("[*] Example: python3 stealth_net.py 192.168.31.137 1234")
		sys.exit(0)
	PUBLIC_KEY = "Stealth_Net_v_1.0.1"
	PUBLIC_KEY_HASH = hashlib.sha256(PUBLIC_KEY.encode()).hexdigest()
	print("[*] Running StealthNet...!\n")
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server.bind((sys.argv[1],int(sys.argv[2])))
	server.listen(5)
	while True:
		(client_socket,addr) = server.accept()
		print(f"Receiving Connection from {addr[0]} : {addr[1]}")
		data = receive_data(client_socket)
		proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,data['remote_host'],int(data["remote_port"])))
		proxy_thread.start()


def proxy_handler(client_socket,remote_host,remote_port):
	remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	remote_socket.connect((remote_host,remote_port))

	remote_buffer = receive_data(remote_socket)
	if len(remote_buffer):
		print(remote_buffer)
		send_data(client_socket,remote_buffer)

	while True:
		local_buffer = receive_data(client_socket)
		if len(local_buffer):
			send_data(remote_socket,local_buffer)
		remote_buffer = receive_data(remote_socket)
		if len(remote_buffer):
			print(remote_buffer)
			send_data(client_socket,remote_buffer)

def receive_data(connection):
    HEADERSIZE=10
    full_data=b''
    meta_data = True
    full_data_recvd = True
    while full_data_recvd:
        data = connection.recv(1024)
        if meta_data:
            data_len=int(data[:HEADERSIZE])
            meta_data=False
        full_data+=data

        if len(full_data)-HEADERSIZE >= data_len:
            data = full_data[HEADERSIZE:]
            data = pickle.loads(data)
            full_data_recvd = False
    return data

def send_data(connection,data):
	data=pickle.dumps(data)
	HEADERSIZE = 10
	data = bytes(f'{len(data):<{HEADERSIZE}}','utf-8') + data
	connection.send(data)

server_loop()