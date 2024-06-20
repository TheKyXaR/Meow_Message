class RegLogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Реєстрація та авторизація")

        # Змінні для збереження даних
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Інтерфейс реєстрації
        self.register_frame = tk.Frame(self.root, padx=10, pady=10)
        tk.Label(self.register_frame, text="Ім'я користувача:").grid(row=0, column=0, sticky='w')
        tk.Entry(self.register_frame, textvariable=self.username_var).grid(row=0, column=1)
        tk.Label(self.register_frame, text="Пароль:").grid(row=1, column=0, sticky='w')
        tk.Entry(self.register_frame, textvariable=self.password_var, show='*').grid(row=1, column=1)
        tk.Button(self.register_frame, text="Зареєструватися", command=self.register).grid(row=2, column=0, columnspan=2, pady=10)
        self.register_frame.pack(pady=20)

        # Інтерфейс авторизації
        self.login_frame = tk.Frame(self.root, padx=10, pady=10)
        tk.Label(self.login_frame, text="Ім'я користувача:").grid(row=0, column=0, sticky='w')
        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1)
        tk.Label(self.login_frame, text="Пароль:").grid(row=1, column=0, sticky='w')
        tk.Entry(self.login_frame, textvariable=self.password_var, show='*').grid(row=1, column=1)
        tk.Button(self.login_frame, text="Увійти", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        self.login_frame.pack(pady=20)

    def register(self):
        # Отримання даних з полів
        username = self.username_var.get()
        password = self.password_var.get()

        data = form_request("register", 
                            login = username,
                            passcode = password)

        if send_data_post(json.dumps(data))["register"] :
            messagebox.showinfo("Реєстрація", f"Користувач {username} зареєстрований успішно!")
        else :
            messagebox.showinfo("Реєстрація", f"Логін {username} вже занятий!")

    def login(self):
        # Отримання даних з полів
        username = self.username_var.get()
        password = self.password_var.get()

        data = form_request("login", 
                            login = username,
                            passcode = password)

        req = send_data_post(json.dumps(data))["login"]

        if req:
            preferences["user"] = {"id": str(req[0]), "login": req[1], "pass": req[2], "nickname": req[3]}
            with open("settings.json", "w", encoding = "utf-8") as file :
                json.dump(preferences, file, separators = (',', ':') ,indent = 4)

            messagebox.showinfo("Авторизація", f"Успішний вхід для користувача {username}.")
            self.root.destroy()
        else:
            messagebox.showerror("ООООО ЙООООЙ", "Логін або пароль. Шото не так кароче :(")