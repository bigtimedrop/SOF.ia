import tkinter as tk
import pyttsx3
from interface import create_interface
from config import load_config, save_config
from responses import get_response, speak
from utils import save_to_history

# Configuração inicial
config = load_config()

def speak_current_response(chat_log):

    try:
        log_content = chat_log.get("1.0", tk.END).strip()
        lines = log_content.split("\n")
        last_response = ""

        for line in reversed(lines):
            if line.startswith("SOF.IA: "):
                last_response_line = line
                break

        if last_response_line:
            response_text = last_response_line.replace("SOF.IA: ", "").strip()
            if response_text:
                speak(response_text)
        else:
            print("Nenhuma resposta encontrada.")
    except Exception as e:
        print(f"Erro ao falar a última resposta: {e}")

root, chat_log, entry_message, send_button, speak_button = create_interface(config, speak_current_response)

# Função de envio de mensagem
def send_message(event=None):
    user_message = entry_message.get()
    if user_message.strip() == "":
        return
    response = get_response(user_message)
    chat_log.insert(tk.END, "Você: " + user_message + "\n")
    chat_log.insert(tk.END, "SOF.IA: " + response + "\n\n")
    save_to_history(user_message, response)
    entry_message.delete(0, tk.END)

entry_message.bind("<Return>", send_message)
send_button.config(command=send_message)

root.mainloop()
