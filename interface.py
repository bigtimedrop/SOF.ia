import tkinter as tk
from tkinter import messagebox
from config import save_config

def create_interface(config):
    root = tk.Tk()
    root.title("SOF.IA Assistente Virtual")
    root.resizable(False, False)

    menu = tk.Menu(root)
    root.config(menu=menu)

    settings_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Configurações", menu=settings_menu)
    settings_menu.add_command(label="Mudar Tema", command=lambda: change_theme(root, chat_log, entry_message, config))
    settings_menu.add_command(label="Manual de Uso", command=show_help)
    settings_menu.add_command(label="Histórico de Conversas", command=show_history)

    chat_log = tk.Text(root, state="normal", height=20, width=50)
    chat_log.pack(pady=10)

    entry_message = tk.Entry(root, width=40)
    entry_message.pack(pady=10)

    send_button = tk.Button(root, text="Enviar")
    send_button.pack(pady=10)

    speak_button = tk.Button(root, text= "Falar", command=lambda: speak_current_response(chat_log))
    speak_button.pack(pady=10)

    apply_theme(root, chat_log, entry_message, config)
    return root, chat_log, entry_message, speak_button

def apply_theme(root, chat_log, entry_message, config):
    if config["theme"] == "dark":
        root.config(bg="black")
        chat_log.config(bg="black", fg="white")
        entry_message.config(bg="gray", fg="white")
    else:
        root.config(bg="white")
        chat_log.config(bg="white", fg="black")
        entry_message.config(bg="white", fg="black")

def change_theme(root, chat_log, entry_message, config):
    config["theme"] = "dark" if config["theme"] == "light" else "light"
    apply_theme(root, chat_log, entry_message, config)
    save_config(config)

def show_help():
    help_text = """Manual de Uso:
    1. Digite sua mensagem na caixa de texto.
    2. Pressione 'Enter' ou clique no botão 'Enviar'.
    3. Veja a resposta da SOF.IA no painel de chat.
    4. Use o menu de Configurações para alterar o tema.
    5. Use "Pesquisar sobre" para pesquisar no seu navegador.
    6. Use "Calcular" para fazer cálculos.
    7. Clique em "Falar" para ouvir a ultima resposta."""
    messagebox.showinfo("Manual de Uso", help_text)

def show_history():
    try:
        with open("history.txt", "r") as f:
            history = f.read()
        messagebox.showinfo("Histórico de Conversas", history)
    except FileNotFoundError:
        messagebox.showinfo("Histórico de Conversas", "Nenhum histórico encontrado.")
