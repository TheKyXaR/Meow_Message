def form_request (req, **data) :
	return {"command": req, "data": data}

def send_data(message) :
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((preferences["addres"], preferences["port"]))
	sock.send(message.encode("utf-8"))
	sock.close()

def send_data_post(message) :
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((preferences["addres"], preferences["port"]))
	sock.send(message.encode("utf-8"))
	result = json.loads(sock.recv(1024).decode("utf-8"))
	sock.close()
	return result