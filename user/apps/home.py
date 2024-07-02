class Messenger:
	def __init__(self, root):
		self.root = root
		self.root.title("Meow Message")
		self.root.geometry("500x600")

		# Додавання меню
		self.menu_bar = Menu(root)
		self.root.config(menu=self.menu_bar)

		# Меню "Меню"
		self.main_menu = Menu(self.menu_bar, tearoff=0)
		self.menu_bar.add_cascade(label="Меню", menu=self.main_menu)
		self.main_menu.add_command(label="Налаштування профілю", command=self.open_profile_settings)
		self.main_menu.add_command(label="Створити чат", command=self.create_chat)
		self.main_menu.add_separator()
		self.main_menu.add_command(label="Вийти", command=root.quit)

		# Меню "Налаштування чатів"
		self.chat_settings_menu = Menu(self.menu_bar, tearoff=0)
		self.menu_bar.add_cascade(label="Налаштування чатів", menu=self.chat_settings_menu)
		self.chat_settings_menu.add_command(label="Змінити назву чату", command=self.rename_chat)
		self.chat_settings_menu.add_command(label="Додати людей до чату", command=self.add_people_to_chat)

		# Додавання вкладок
		self.notebook_frame = ttk.Frame(root)
		self.notebook_frame.pack(fill=tk.BOTH, expand=True)
		self.notebook = ttk.Notebook(self.notebook_frame)
		self.notebook.pack(fill=tk.BOTH, expand=True)
		self.chat_tabs = {}
		
		# Лейбл для відображення назви активного чату
		self.active_chat_label = tk.Label(root, text="Active Chat: ", font=("Arial", 14))
		self.active_chat_label.pack(pady=10)
		
		# Зв'язок зміни активної вкладки з оновленням лейблу
		self.notebook.bind("<<NotebookTabChanged>>", self.update_active_chat_label)
		
		# Додавання першого чату
		self.create_chat(chat_name = "всіхній")
		self.create_chat(chat_name = "наший")
		self.stop_thread = False
		self.login = tk.StringVar()
		self.password = tk.StringVar()
		self.nickname = tk.StringVar()

	def create_chat(self, chat_name = ""):
		chat_name = chat_name if chat_name else simpledialog.askstring("Створити чат", "Введіть назву чату:", parent=self.root)
		if chat_name:
			self.add_new_chat(chat_name)

	def add_new_chat(self, chat_name):
		chat_frame = ttk.Frame(self.notebook)
		self.notebook.add(chat_frame, text=chat_name)

		text_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state='disabled', height=20)
		text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		entry = tk.Entry(chat_frame, width=40)
		entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
		send_button = tk.Button(chat_frame, text="Send", command=lambda: self.send_message())
		send_button.pack(side=tk.RIGHT, padx=10, pady=10)
		entry.bind("<Return>", lambda event: self.send_message())

		self.chat_tabs[chat_frame] = (text_area, entry)
		self.update_active_chat_label()  # Оновлення назви активного чату після додавання нового

	def change_profile_settings(self, win):
		data = form_request("change_profile_settings",
							find_login = preferences['user']['login'], 
							nickname = self.nickname.get(), 
							login = self.login.get(),
							passcode = self.password.get())
		if send_data_post(json.dumps(data)) :
			user_sett = {
				"id": preferences['user']['id'],
				"login": self.login.get() if self.login.get() else preferences['user']['login'],
				"pass": self.password.get() if self.password.get() else preferences['user']['pass'],
				"nickname": self.nickname.get() if self.nickname.get() else preferences['user']['nickname'],
			}
			preferences['user'] = user_sett
			with open("settings.json", "w", encoding = "utf-8") as file :
				json.dump(preferences, file, separators = (',', ':') ,indent = 4)

			messagebox.showinfo("Збереження", "Дані успішно замінені")
			win.destroy()
		else :
			messagebox.showerror("Збереження", "Дані не замінені")

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
		tk.Button(settings_window, text="Зберегти", command=lambda: self.change_profile_settings(settings_window)).pack(pady=5)

	def rename_chat(self):
		selected_tab = self.notebook.select()
		if selected_tab:
			tab_index = self.notebook.index(selected_tab)
			rename_window = tk.Toplevel(self.root)
			rename_window.title("Змінити назву чату")
			rename_window.geometry("300x100")
			tk.Label(rename_window, text="Нова назва:").pack(padx=10, pady=5)
			new_name_entry = tk.Entry(rename_window)
			new_name_entry.pack(padx=10, pady=5)
			tk.Button(rename_window, text="Змінити", command=lambda: self.update_chat_name(tab_index, new_name_entry.get())).pack(padx=10, pady=10)

	def update_chat_name(self, tab_index, new_name):
		if new_name:
			self.notebook.tab(tab_index, text=new_name)
			self.update_active_chat_label()  # Оновлення назви активного чату після зміни назви

	def add_people_to_chat(self):
		add_people_window = tk.Toplevel(self.root)
		add_people_window.title("Додати людей до чату")
		add_people_window.geometry("300x200")
		tk.Label(add_people_window, text="Це вікно для додавання людей до чату.").pack(padx=10, pady=10)

	def update_active_chat_label(self, event=None):
		# Отримуємо назву активної вкладки і відображаємо її у лейблі
		current_tab = self.notebook.select()
		chat_name = self.notebook.tab(current_tab, "text")
		if event :
			return chat_name
		self.active_chat_label.config(text=f"{chat_name}")


	def get_data(self):
		while not self.stop_thread:
			print(update_active_chat_label(event = True), "123")
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