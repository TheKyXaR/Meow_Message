class Messenger:
	def __init__(self, root):
		self.root = root
		self.root.title("Meow Message")
		self.root.geometry("400x500")
		
		# Додавання меню
		self.menu_bar = Menu(root)
		self.root.config(menu=self.menu_bar)
		self.file_menu = Menu(self.menu_bar, tearoff=0)
		self.menu_bar.add_cascade(label="Меню", menu=self.file_menu)
		self.file_menu.add_command(label="Налаштування профілю", command=self.open_profile_settings)
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Вийти", command=root.quit)

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

		self.login = tk.StringVar()
		self.password = tk.StringVar()
		self.nickname = tk.StringVar()

	def change_profile_settings(self):
		data = form_request("change_profile_settings", 
							nickname = self.nickname.get(), 
							login = self.login.get(),
							password = self.password.get())
		send_data(json.dumps(data))

	def open_profile_settings(self):
		# Створення нового вікна для налаштувань профілю
		settings_window = tk.Toplevel(self.root)
		settings_window.title("Налаштування профілю")
		settings_window.geometry("200x300")

		# Додайте елементи для налаштувань
		tk.Label(settings_window, text="Ім'я користувача:").pack(pady=5)
		tk.Entry(settings_window, textvariable=self.nickname).pack(pady=1)
		tk.Label(settings_window, text="Логін:").pack(pady=5)
		tk.Entry(settings_window, textvariable=self.login).pack(pady=1)
		tk.Label(settings_window, text="Пароль:").pack(pady=5)
		tk.Entry(settings_window, textvariable=self.password).pack(pady=1)
		tk.Button(settings_window, text="Зберегти", command=self.change_profile_settings).pack(pady=5)

	def get_data(self):
		while not self.stop_thread:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((preferences["addres"], preferences["port"]))
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

	def send_message(self):
		message = self.entry.get()
		if message:
			current_time = datetime.now().strftime('%H:%M:%S')
			data = form_request("send_message", 
								nickname = preferences["user"]["nickname"], 
								time_ms = current_time,
								text_ms = message)

			send_data(json.dumps(data))
			self.entry.delete(0, tk.END)

	def on_closing(self):
		self.stop_thread = True
		self.root.destroy()