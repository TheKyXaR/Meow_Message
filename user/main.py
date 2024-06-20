#User

import json
import socket
import threading
import tkinter as tk
from time import sleep
from datetime import datetime
from tkinter import messagebox
from tkinter import scrolledtext

with open("settings.json") as file :
	preferences = json.loads(file.read())

exec(open("./request__.py").read())
exec(open("./apps/home.py").read())
exec(open("./apps/reg_log.py", encoding="utf-8").read())

if __name__ == '__main__':

	for x in preferences["user"].values() :
		if x != "" :
			break
	else :
		root = tk.Tk()
		reg_log = RegLogApp(root)
		root.mainloop()


	root = tk.Tk()
	main = Messenger(root)

	thread = threading.Thread(target = main.get_data)
	thread.daemon = True
	thread.start()
	root.protocol("WM_DELETE_WINDOW", main.on_closing)

	root.mainloop()