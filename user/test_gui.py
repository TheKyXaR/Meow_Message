import tkinter as tk
from tkinter import Menu, scrolledtext, ttk, simpledialog

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
        self.create_chat(initial=True)
        self.stop_thread = False
        self.login = tk.StringVar()
        self.password = tk.StringVar()
        self.nickname = tk.StringVar()

    def create_chat(self, initial=False):
        chat_name = simpledialog.askstring("Створити чат", "Введіть назву чату:", parent=self.root) if not initial else "Chat 1"
        if chat_name:
            self.add_new_chat(chat_name)

    def add_new_chat(self, chat_name):
        chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(chat_frame, text=chat_name)

        text_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state='disabled', height=20)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        entry = tk.Entry(chat_frame, width=40)
        entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        send_button = tk.Button(chat_frame, text="Send", command=lambda: self.send_message(text_area, entry))
        send_button.pack(side=tk.RIGHT, padx=10, pady=10)
        entry.bind("<Return>", lambda event: self.send_message(text_area, entry))

        self.chat_tabs[chat_frame] = (text_area, entry)
        self.update_active_chat_label()  # Оновлення назви активного чату після додавання нового

    def send_message(self, text_area, entry):
        message = entry.get()
        if message:
            text_area.config(state='normal')
            text_area.insert(tk.END, f"You: {message}\n")
            text_area.config(state='disabled')
            entry.delete(0, tk.END)

    def open_profile_settings(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Налаштування профілю")
        profile_window.geometry("300x200")
        tk.Label(profile_window, text="Це вікно налаштувань профілю.").pack(padx=10, pady=10)

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
        self.active_chat_label.config(text=f"{chat_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Messenger(root)
    root.mainloop()
