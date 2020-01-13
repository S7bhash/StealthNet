import socket
import pickle
from encryption import encrypt,decrypt
import hashlib
import sys

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

if __name__ == '__main__':
	print("******* WELCOME TO STEALTHNET ********\n\t\t\t\t-S7bhash\n")
	if len(sys.argv) ==1 or sys.argv=="help":
		print("[-] Please enter the host address and port address....")
		print("Ex: python3 server.py 127.0.0.1 8080")
		sys.exit(0)
	PUBLIC_KEY = "Stealth_Net_v_1.0.1"
	PUBLIC_KEY_HASH = hashlib.sha256(PUBLIC_KEY.encode()).hexdigest()

	private_key = "Stealth_Net_Server_v_1.0"
	PRIVATE_KEY_HASH = hashlib.sha1(private_key.encode()).hexdigest()

	print("[*] waiting for connection..!")
	listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	listener.bind((sys.argv[1],int(sys.argv[2])))
	listener.listen(0)
	conn,addr = listener.accept()
	print("Got Connection...\n")

	while True:
		msg = input(">")
		data ={}
		data['msg'] = encrypt(msg,PRIVATE_KEY_HASH)
		data['msg'] = encrypt(data['msg'],PUBLIC_KEY_HASH)
		data['private_key'] = encrypt(PRIVATE_KEY_HASH,PUBLIC_KEY_HASH)
		send_data(conn,data)
		data = receive_data(conn)
		key = decrypt(data['private_key'],PUBLIC_KEY_HASH)
		data = decrypt(decrypt(data['msg'],PUBLIC_KEY_HASH),key)
		print(f"> {data}")
		


