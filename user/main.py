#User

import json
import socket
import threading
import tkinter as tk
from time import sleep
from datetime import datetime
from tkinter import messagebox
from tkinter import scrolledtext, Menu

with open("settings.json") as file :
	preferences = json.loads(file.read())

exec(open("./request__.py").read())
exec(open("./apps/home.py", encoding="utf-8").read())
exec(open("./apps/reg_log.py", encoding="utf-8").read())

if __name__ == '__main__':
	root = tk.Tk()
	reg_log = RegLogApp(root)

	login = False
	if preferences['user']['id'] and preferences['user']['pass'] :
		login = reg_log.login(preferences['user']['login'], preferences['user']['pass'])

	root.mainloop()	

	if login != False :
		root.mainloop()

		root = tk.Tk()
		main = Messenger(root)

		thread = threading.Thread(target = main.get_data)
		thread.daemon = True
		thread.start()
		root.protocol("WM_DELETE_WINDOW", main.on_closing)

		root.mainloop()