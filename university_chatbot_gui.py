import tkinter as tk
from chatbot_engine import get_response

root = tk.Tk()
root.title("University FAQ Chatbot")

chat_display = tk.Text(root, height=20, width=60)
chat_display.pack()

entry = tk.Entry(root, width=50)
entry.pack()

def send_message():
    user_text = entry.get()
    if not user_text.strip():
        return

    response = get_response(user_text)

    chat_display.insert(tk.END, f"You: {user_text}\nBot: {response}\n\n")
    entry.delete(0, tk.END)


send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()
