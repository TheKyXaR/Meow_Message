import tkinter as tk
from tkinter import messagebox

class LoginApp:
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

        # Логіка реєстрації (можна зберігати в базі даних, файлі тощо)
        # В даному випадку просто виводимо інформаційне вікно
        messagebox.showinfo("Реєстрація", f"Користувач {username} зареєстрований успішно!")

    def login(self):
        # Отримання даних з полів
        username = self.username_var.get()
        password = self.password_var.get()

        # Логіка авторизації (можна перевіряти в базі даних, файлі тощо)
        # В даному випадку просто перевіряємо пароль і виводимо відповідне повідомлення
        if username == "" or password == "":
            messagebox.showerror("Помилка", "Будь ласка, введіть ім'я користувача та пароль.")
        else:
            messagebox.showinfo("Авторизація", f"Успішний вхід для користувача {username}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
