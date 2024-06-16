import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

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

    def send_message(self):
        message = self.entry.get()
        if message:
            self.text_area.configure(state='normal')
            current_time = datetime.now().strftime('%H:%M:%S')
            self.text_area.insert(tk.END, f"Ви ({current_time}): {message}\n")
            self.text_area.yview(tk.END)  # Автоматичне прокручування до кінця
            self.text_area.configure(state='disabled')
            self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Messenger(root)
    root.mainloop()
