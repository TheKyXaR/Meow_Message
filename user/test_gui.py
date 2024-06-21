import tkinter as tk
from tkinter import scrolledtext, Menu

class ChatApplication:
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
    
    def send_message(self):
        # Логіка для відправки повідомлення
        message = self.entry.get()
        if message:
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, "You: " + message + "\n")
            self.text_area.config(state='disabled')
            self.entry.delete(0, tk.END)

    def open_profile_settings(self):
        # Створення нового вікна для налаштувань профілю
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Налаштування профілю")
        settings_window.geometry("300x200")
        
        # Додайте елементи для налаштувань
        tk.Label(settings_window, text="Ім'я користувача:").pack(pady=10)
        tk.Entry(settings_window).pack(pady=5)
        
        tk.Label(settings_window, text="Електронна пошта:").pack(pady=10)
        tk.Entry(settings_window).pack(pady=5)
        
        tk.Button(settings_window, text="Зберегти", command=settings_window.destroy).pack(pady=20)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()
