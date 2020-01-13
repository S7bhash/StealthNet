import random

length = 91
uid = 10101
server_key = 210012

def init_alphasymbols(character):
	alphaSymbols = [';','A','B','{','[','C','D','E',':','F','=',"G",'H','I','J','K','>','L','M','N',')','O','P','Q','R',']','}','S','T','U','V','W','X','Y','Z',
					'a','b','c','d','e','f','g','h','i','j','-','k','l','m','n','o',"_",'p','q','r','s','?','t','u','v','w','x','y','z',
					'1','2','(','3','4','<','5','6','7','8','|','9','0','@','$','%','&','*'," ",'/','#','.',',',"'",'"','!','+']
	global length
	length = len(alphaSymbols)
	return alphaSymbols.index(character)

def get_char_to_decrypt(index):
	alphaSymbols = [';','A','B','{','[','C','D','E',':','F','=',"G",'H','I','J','K','>','L','M','N',')','O','P','Q','R',']','}','S','T','U','V','W','X','Y','Z',
					'a','b','c','d','e','f','g','h','i','j','-','k','l','m','n','o',"_",'p','q','r','s','?','t','u','v','w','x','y','z',
					'1','2','(','3','4','<','5','6','7','8','|','9','0','@','$','%','&','*'," ",'/','#','.',',',"'",'"','!','+']

	return alphaSymbols[index]

def algo(character,key,server_key):
	global length
	global uid
	ind = init_alphasymbols(character)
	new_ind = (ind + key + server_key+uid)%length
	return new_ind

def rev_algo(index,key,server_key):
	global length
	d = (key + server_key - index)%length
	if d!=0:
		return length-d
	else:
		return 0

def get_alphasymbol(index):
	alphaSymbols =  ['c','d','e','(','f','g','h',';','A','B','{','[','C','D','E','F','=','P','Q','R',']','}','S','T','U','V','W','X','Y','Z','<','5','6','7','8','|','9',
					'a','b','i','j','-','k','l','m',':','n','o',"_",'p','q','r','s','?','t','u','v','w','x','y','z',
					'1','2','3','4','0','@',"G",'H','I','J',')','K','>','L','M','N','O','$','%','&','*'," ",'/','#','.',',',"'",'"','!','+']
	return alphaSymbols[index]

def get_index_to_decrpt(character):
	alphaSymbols = ['c','d','e','(','f','g','h',';','A','B','{','[','C','D','E','F','=','P','Q','R',']','}','S','T','U','V','W','X','Y','Z','<','5','6','7','8','|','9',
					'a','b','i','j','-','k','l','m',':','n','o',"_",'p','q','r','s','?','t','u','v','w','x','y','z',
					'1','2','3','4','0','@',"G",'H','I','J',')','K','>','L','M','N','O','$','%','&','*'," ",'/','#','.',',',"'",'"','!','+']
	return alphaSymbols.index(character)

def getKeyHash(key):
	key_sum=len(key)
	passhash = ["G",'H','I','1','2','3','*'," ",'/','#','o','p','4','5','J','K','L','L','M','=','N','O','P','Q','X','Y','Z',
				'a','b','c','A','B','-','i','j','k','l','m','n','u','v','w','x','y','z','C','D','E','F','d','e','f','g','h',
				'6','7','8','9','0','@','$','%','&','q','r','s','t','.',',',"'",'"','_','!','R','S','T','U','V','W']

	for x in key:
		key_sum+=passhash.index(x)
	return key_sum


def encrypt(data,key):
	global server_key
	key = getKeyHash(key)
	encoded_data=""
	for i in str(data):
		encoded_data+=get_alphasymbol(algo(i,key,server_key))
	return encoded_data


def decrypt(data,key):
	global server_key
	key = getKeyHash(key)
	decoded_data=""
	for i in str(data):
		ind = get_index_to_decrpt(i)
		decoded_data+=get_char_to_decrypt(rev_algo(ind,key,server_key))
	return decoded_data






