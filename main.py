import tkinter as tk
from interface import create_interface
from config import load_config, save_config
from responses import get_response
from utils import save_to_history

# Configuração inicial
config = load_config()

# Criar a interface
root, chat_log, entry_message = create_interface(config)

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

root.mainloop()
