import tkinter as tk
from tkinter import scrolledtext, Frame
from chatbot_engine import get_response

# ---------------- Window Setup ----------------
root = tk.Tk()
root.title("🎓 University FAQ Chatbot")
root.geometry("550x650")
root.config(bg="#E8EBF5")

# ---------------- Header Bar ----------------
header = tk.Frame(root, bg="#4A6FA5", height=60)
header.pack(fill="x")

title = tk.Label(
    header, text="University FAQ Assistant 🤖", 
    bg="#4A6FA5", fg="white",
    font=("Segoe UI", 16, "bold")
)
title.pack(pady=10)

# ---------------- Chat Display ----------------
chat_frame = Frame(root, bg="#E8EBF5")
chat_frame.pack(padx=15, pady=15, fill="both", expand=True)

chat_display = scrolledtext.ScrolledText(
    chat_frame, wrap=tk.WORD, font=("Segoe UI", 11),
    bg="#FFFFFF", fg="#333333", bd=0, relief="flat",
)
chat_display.config(state="disabled")
chat_display.pack(fill="both", expand=True)

# ---------------- Input Section ----------------
input_frame = Frame(root, bg="#E8EBF5")
input_frame.pack(fill="x", pady=10)

entry = tk.Entry(
    input_frame, font=("Segoe UI", 12), width=38,
    bg="white", fg="#333333", relief="flat",
    highlightthickness=2, highlightbackground="#C2C9D6"
)
entry.grid(row=0, column=0, padx=10, ipady=10)


def format_message(sender, message, align="left", bg_color="#D9E6F2", fg_color="#000"):
    chat_display.tag_configure(sender, justify=align, foreground=fg_color)
    chat_display.insert(tk.END, f"{message}\n\n", sender)

    # Highlight bubble
    start = f"end-{(len(message)//40)+2}l"
    chat_display.tag_add(sender, start, "end")
    chat_display.tag_configure(sender, background=bg_color, lmargin1=10, rmargin=10, spacing3=6)


def send_message(event=None):
    user_text = entry.get()
    entry.delete(0, tk.END)

    if not user_text.strip():
        return

    chat_display.config(state="normal")

    # Format user message bubble
    format_message("user", f"🧑 You:\n{user_text}", align="left", bg_color="#C8E6C9")

    # Get response
    response = get_response(user_text)

    # Format bot message bubble
    format_message("bot", f"🤖 Bot:\n{response}", align="left", bg_color="#FFE9C9")

    chat_display.config(state="disabled")
    chat_display.see(tk.END)


# ---------------- Button ----------------
send_button = tk.Button(
    input_frame, text="Send", command=send_message,
    bg="#4A6FA5", fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat", width=10, height=1,
)
send_button.grid(row=0, column=1)


root.bind("<Return>", send_message)

root.mainloop()
