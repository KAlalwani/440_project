# app.py
import tkinter as tk
from tkinter import scrolledtext

from chatbot_engine import UniversityFAQBot

def main():
    bot = UniversityFAQBot(show_trace=False)  # change to True only if you want the trace

    root = tk.Tk()
    root.title("🎓 University FAQ Assistant")
    root.geometry("560x680")
    root.configure(bg="#E8EBF5")

    header = tk.Frame(root, bg="#4A6FA5", height=60)
    header.pack(fill="x")
    tk.Label(header, text="University FAQ Assistant 🤖", bg="#4A6FA5", fg="white",
             font=("Segoe UI", 16, "bold")).pack(pady=10)

    chat_frame = tk.Frame(root, bg="#E8EBF5")
    chat_frame.pack(padx=14, pady=12, fill="both", expand=True)

    chat = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Segoe UI", 11),
                                     bg="white", fg="#1F2937", bd=0, relief="flat")
    chat.pack(fill="both", expand=True)
    chat.config(state="disabled")

    input_frame = tk.Frame(root, bg="#E8EBF5")
    input_frame.pack(fill="x", pady=10)

    entry = tk.Entry(input_frame, font=("Segoe UI", 12), bg="white", fg="#111827",
                     relief="flat", highlightthickness=2, highlightbackground="#C2C9D6")
    entry.grid(row=0, column=0, padx=10, ipady=8, sticky="ew")
    input_frame.grid_columnconfigure(0, weight=1)

    def insert_bubble(sender: str, text: str, bg: str, fg: str = "#111827", align: str = "left"):
        chat.config(state="normal")

        # Each message gets its own tag → prevents styling "bleeding" between messages
        tag = f"{sender}_{insert_bubble.counter}"
        insert_bubble.counter += 1

        start = chat.index("end-1c")
        chat.insert(tk.END, text + "\n\n")
        end = chat.index("end-1c")

        chat.tag_add(tag, start, end)
        chat.tag_config(tag, background=bg, foreground=fg, lmargin1=10, lmargin2=10, rmargin=10, spacing3=6, justify=align)

        chat.config(state="disabled")
        chat.see(tk.END)

    insert_bubble.counter = 0

    def send(event=None):
        user_text = entry.get().strip()
        if not user_text:
            return
        entry.delete(0, tk.END)

        insert_bubble("user", f"🧑 You:\n{user_text}", "#C8E6C9", align="left")

        response = bot.get_response(user_text)
        insert_bubble("bot", f"🤖 Bot:\n{response}", "#FFE9C9", align="left")

    send_btn = tk.Button(input_frame, text="Send", command=send,
                         bg="#4A6FA5", fg="white", font=("Segoe UI", 12, "bold"),
                         relief="flat", width=10)
    send_btn.grid(row=0, column=1, padx=10)

    root.bind("<Return>", send)
    root.mainloop()

if __name__ == "__main__":
    main()
