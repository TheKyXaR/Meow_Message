#User

import socket
import request__
import threading
import json
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from time import sleep

with open("settings.json") as file :
	user_settings = json.loads(file.read())

class Messenger:
	def __init__(self, root):
		self.root = root
		self.root.title("Green NET")
		self.root.geometry("400x500")

		# Вікно для відображення повідомлень
		self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
		self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		# Поле вводу
		self.entry = tk.Entry(root, width=40)
		self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
		# Кнопка відправки
		self.send_button = tk.Button(root, text="Send", command=self.send_message)
		self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)
		# Обробка натискання Enter
		self.entry.bind("<Return>", lambda event: self.send_message())

		self.stop_thread = False

	def get_data(self) :
		while not self.stop_thread:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((user_settings["addres"], user_settings["port"]))
			sock.send(json.dumps({"command": "get_messages"}).encode("utf-8"))
			result = json.loads(sock.recv(1024).decode("utf-8"))
			sock.close()
			result = "".join([f"{mss[0]} ({mss[1]}): {mss[2]}\n" for mss in result])
			self.text_area.configure(state='normal')
			self.text_area.delete(1.0, tk.END)
			self.text_area.insert(tk.END, result)
			self.text_area.yview(tk.END)
			self.text_area.configure(state='disabled')
			sleep(0.5)

	def send_data(self, message) :
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((user_settings["addres"], user_settings["port"]))
		sock.send(message.encode("utf-8"))
		sock.close()

	def send_message(self):
		message = self.entry.get()
		if message:
			current_time = datetime.now().strftime('%H:%M:%S')
			data = request__.js_req
			data["command"] = "send_message"
			data["data"]["nickname"] = user_settings["nickname"]
			data["data"]["time_ms"] = current_time
			data["data"]["text_ms"] = message

			self.send_data(json.dumps(data))
			self.entry.delete(0, tk.END)

	def on_closing(self):
		self.stop_thread = True  # Зупинка потоку
		self.root.destroy()

if __name__ == '__main__':
	root = tk.Tk()
	app = Messenger(root)
	thread = threading.Thread(target = app.get_data)
	thread.daemon = True
	thread.start()
	root.protocol("WM_DELETE_WINDOW", app.on_closing)
	root.mainloop()