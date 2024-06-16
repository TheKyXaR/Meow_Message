#Server

import socket
import keyboard
import sqlite3
import json
import os

con = sqlite3.connect("database.db")
cur = con.cursor()

ip = '127.0.0.1'
port = 9090

sock = socket.socket()
sock.bind((ip, port))
sock.listen()

def close_server () :
	sock.close()
keyboard.add_hotkey("ctrl+shift+c", close_server)

def clear_cons () :
	os.system("cls")
keyboard.add_hotkey("ctrl+x", clear_cons)

def main() :
	while True :
		user, addr = sock.accept()
		data = user.recv(1024).decode("utf-8")
		data = json.loads(data)

		if data["command"] == "send_message":
			data_ms = data["data"]
			cur.execute("""INSERT INTO message (author, time_ms, text_ms)
				           VALUES (?, ?, ?)""", 
				           (data_ms["nickname"], data_ms["time_ms"], data_ms["text_ms"]))
			con.commit()
		elif data["command"] == "get_messages":
			data = cur.execute("""SELECT author, time_ms, text_ms
								  FROM (SELECT * 
										FROM message
										ORDER BY id DESC
										LIMIT 27) AS subquery
								  ORDER BY id ASC""").fetchall()
			user.send(json.dumps(data).encode("utf-8"))

if __name__ == '__main__':
	print(f"server start on {ip}:{port}")
	main()