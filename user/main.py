#User

import json
import socket
import threading
import tkinter as tk
from time import sleep
from datetime import datetime
from tkinter import messagebox
from tkinter import scrolledtext

exec(open("./request__.py").read())
exec(open("./apps/home.py").read())
exec(open("./apps/reg_log.py", encoding="utf-8").read())

if __name__ == '__main__':
	root = tk.Tk()

	reg_log = RegLogApp(root)
	
	root.mainloop()


	root = tk.Tk()
	homework = Messenger(root)

	thread = threading.Thread(target = homework.get_data)
	thread.daemon = True
	thread.start()
	root.protocol("WM_DELETE_WINDOW", homework.on_closing)

	root.mainloop()