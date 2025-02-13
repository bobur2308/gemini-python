import google.generativeai as genai
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext

# Load environment variables
load_dotenv()

# Get the API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")

# Function to handle sending a message
def send_message(event=None):  # `event=None` allows Enter key binding
    user_text = entry.get()
    if not user_text.strip():
        return  # Ignore empty messages

    # Show user's message in chatbox
    chat_box.insert(tk.END, "You: " + user_text + "\n", "user")
    entry.delete(0, tk.END)  # Clear input field
    chat_box.yview(tk.END)

    # Add typing indicator for AI
    chat_box.insert(tk.END, "Bot is typing...\n", "bot")
    chat_box.yview(tk.END)

    # Delay AI response for animation effect
    root.after(1000, lambda: generate_response(user_text))

# Function to generate AI response
def generate_response(user_text):
    response = model.generate_content(user_text)
    bot_reply = response.text.strip()

    # Remove the "typing..." indicator
    chat_box.delete("end-2l", tk.END)

    # Show AI response in chatbox with animation
    chat_box.insert(tk.END, "Bot: ", "bot")
    root.after(300, lambda: type_response(bot_reply, 0))

# Function to animate AI typing effect
def type_response(text, index):
    if index < len(text):
        chat_box.insert(tk.END, text[index], "bot")
        root.after(30, lambda: type_response(text, index + 1))  # Simulate typing effect
    else:
        chat_box.insert(tk.END, "\n")
        chat_box.yview(tk.END)

# Function to clear the chat history
def clear_chat():
    chat_box.delete(1.0, tk.END)

# GUI Setup using Tkinter
root = tk.Tk()
root.title("AI Chatbot (Gemini)")
root.geometry("500x600")

# Chat History Box
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="normal", width=60, height=25, font=("Arial", 12))
chat_box.tag_config("user", foreground="blue")
chat_box.tag_config("bot", foreground="green")
chat_box.pack(padx=10, pady=10)

# Input Field
entry = tk.Entry(root, width=50, font=("Arial", 14))
entry.pack(padx=10, pady=5)
entry.bind("<Return>", send_message)  # Bind Enter key to send message

# Send Button
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 14), bg="lightblue")
send_button.pack(pady=5)

# Clear Chat Button
clear_button = tk.Button(root, text="Clear Chat", command=clear_chat, font=("Arial", 14), bg="red")
clear_button.pack(pady=5)

# Run the App
root.mainloop()
