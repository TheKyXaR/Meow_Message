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

		elif data["command"] == "register":
			data_reg = data["data"]

			check_login = cur.execute("""SELECT login 
									  FROM users 
									  WHERE login = ?""", (data_reg['login'],)).fetchall()

			if not check_login :
				cur.execute("""INSERT INTO users (login, passcode, nickname)
					           VALUES (?, ?, ?)""", 
					           (data_reg["login"], data_reg["passcode"], data_reg["login"]))
				con.commit()
				user.send(json.dumps({"register": True}).encode("utf-8"))
			else :
				user.send(json.dumps({"register": False}).encode("utf-8"))

		elif data["command"] == "login" :
			data_log = data["data"]

			check_login = cur.execute("""SELECT * 
										 FROM users 
										 WHERE login = ?""", (data_log["login"],)).fetchall()

			try:
				check_login = check_login[0]
				if check_login[1] == data_log["login"] and check_login[2] == data_log["passcode"] :
					user.send(json.dumps({"login": check_login}).encode("utf-8"))
				else :
					user.send(json.dumps({"login": False}).encode("utf-8"))
			except IndexError:
				user.send(json.dumps({"login": False}).encode("utf-8"))

		elif data['command'] == 'change_profile_settings' :
			data_ch_prof_sett = data['data']
			data_ch_prof_sett = {k: v for k, v in data_ch_prof_sett.items() if v}
			find_login = data_ch_prof_sett.pop("find_login")
			columns = ", ".join([f"{k} = ?" for k in data_ch_prof_sett.keys()])
			values = list(data_ch_prof_sett.values())
			values.append(str(find_login))

			sql = f"UPDATE users SET {columns} WHERE login = ?"

			try:
				cur.execute(sql, tuple(values))
				con.commit()
				user.send(json.dumps({"login": True}).encode("utf-8"))
			except:
				user.send(json.dumps({"login": False}).encode("utf-8"))

if __name__ == '__main__':
	print(f"server start on {ip}:{port}")
	main()