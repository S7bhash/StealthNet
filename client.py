import socket
import pickle
import sys
import hashlib
import getpass
from encryption import encrypt,decrypt


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
	PUBLIC_KEY = "Stealth_Net_v_1.0.1"
	PUBLIC_KEY_HASH = hashlib.sha256(PUBLIC_KEY.encode()).hexdigest()
	if len(sys.argv) == 1 or sys.argv=="help":
		print("[-] Please specify the remote host and port...!")
		print("[*] Example: python3 client.py 192.168.31.137 1234")
		sys.exit(0)

	private_key = getpass.getpass("[+] Enter the private key:")
	PRIVATE_KEY_HASH = hashlib.sha1(private_key.encode()).hexdigest()	
	host = sys.argv[1]
	port = int(sys.argv[2])	
	print(port)
	connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connection.connect(("192.168.28.135",1234))

	print("Got connection...!")
	data = {}
	data['remote_host'] = host 
	data['remote_port'] = port
	send_data(connection,data)
	while True:
		
		data = receive_data(connection)
		key = decrypt(data['private_key'],PUBLIC_KEY_HASH)
		data = decrypt(decrypt(data['msg'],PUBLIC_KEY_HASH),key)
		print(f"> {data}")
		msg = input(">")
		data ={}
		data['msg'] = encrypt(msg,PRIVATE_KEY_HASH)
		data['msg'] = encrypt(data['msg'],PUBLIC_KEY_HASH)
		data['private_key'] = encrypt(PRIVATE_KEY_HASH,PUBLIC_KEY_HASH)
		send_data(connection,data)



