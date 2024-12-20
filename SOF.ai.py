import tkinter as tk
from tkinter import messagebox, filedialog
import json
import random
import os
import speech_recognition as sr
import math

# Funções principais
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"theme": "light"}

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)

def add_response_category(category, responses):
	data = load_responses()
	data[category] = responses
	with open ("responses.json", "w") as f:
		json.dump(data, f)
	return f"Categoria '{category}' adicionada com sucesso."


def get_response(user_message):
    user_message = user_message.lower()
    responses = load_responses()
    
    if "olá" in user_message or "oi" in user_message:
        return random.choice(responses.get("greetings", []))
    elif "tudo bem" in user_message:
        return random.choice(responses.get("wellbeing", []))
    elif "nome" in user_message:
        return random.choice(responses.get("name", []))
    elif "tempo" in user_message:
        return random.choice(responses.get("weather", []))
    elif "ajuda" in user_message:
        return random.choice(responses.get("help", []))
    elif "adeus" in user_message or "tchau" in user_message:
        return random.choice(responses.get("farewell", []))
    elif "projeto" in user_message:
        return random.choice(responses.get("project", []))
    elif "calcular" in user_message:
        try:
            expression = user_message.replace("calcular", "").strip()
            result = eval(expression, {"__builtins__": None}, {})
            return f"O resultado é: {result}"
        except Exception as e:
            return "Desculpe, não consegui calcular a expressão."
    else:
        return random.choice(responses.get("default", []))

def load_responses():
    try:
        with open("responses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "greetings": ["Olá! Como posso ajudar você hoje?", "Oi! O que você precisa?", "Olá! Em que posso ser útil?"],
            "wellbeing": ["Estou bem, obrigado por perguntar! E você?", "Tudo ótimo por aqui! E com você?", "Estou bem! Como você está?"],
            "name": ["Eu sou a SOF.IA, seu assistente virtual.", "Meu nome é SOF.IA.", "Pode me chamar de SOF.IA."],
            "weather": ["Desculpe, mas não posso fornecer informações sobre o tempo no momento.", "Não tenho acesso a informações meteorológicas.", "Infelizmente, não posso informar sobre o tempo agora."],
            "help": ["Claro! Estou aqui para ajudar. O que você precisa?", "Como posso te ajudar hoje?", "Estou à disposição para ajudar. O que você precisa?"],
            "farewell": ["Até logo! Se precisar de mais alguma coisa, é só chamar.", "Tchau! Tenha um ótimo dia.", "Adeus! Volte sempre que precisar."],
            "project": ["Você está trabalhando no projeto SOF.IA. Como posso ajudá-lo com isso?", "O projeto SOF.IA está progredindo bem. Em que posso ajudar?", "Posso ajudar com o projeto SOF.IA. O que você precisa saber?"],
            "default": ["Desculpe, não compreendi a sua pergunta. Pode reformular?", "Não entendi. Pode explicar de outra forma?", "Pode repetir a pergunta? Não consegui entender."]
        }

def save_to_history(user_message, response):
    with open("history.txt", "a") as f:
        f.write(f"Você: {user_message}\nSOF.IA: {response}\n\n")

def send_message(event=None):
    user_message = entry_message.get()
    if user_message.strip() == "":
        return
    response = get_response(user_message)
    chat_log.insert(tk.END, "Você: " + user_message + "\n")
    chat_log.insert(tk.END, "SOF.IA: " + response + "\n\n")
    save_to_history(user_message, response)
    entry_message.delete(0, tk.END)

def change_theme():
    if config["theme"] == "light":
        config["theme"] = "dark"
    else:
        config["theme"] = "light"
    apply_theme()

def apply_theme():
    if config["theme"] == "dark":
        root.config(bg="black")
        chat_log.config(bg="black", fg="white")
        entry_message.config(bg="gray", fg="white")
    else:
        root.config(bg="white")
        chat_log.config(bg="white", fg="black")
        entry_message.config(bg="white", fg="black")
    save_config(config)

def show_help():
    help_text = """Manual de Uso:
    1. Digite sua mensagem na caixa de texto.
    2. Pressione 'Enter' ou clique no botão 'Enviar'.
    3. Veja a resposta da SOF.IA no painel de chat.
    4. Use o menu de Configurações para alterar o tema.
    """
    messagebox.showinfo("Manual de Uso", help_text)

def show_history():
    try:
        with open("history.txt", "r") as f:
            history = f.read()
        messagebox.showinfo("Histórico de Conversas", history)
    except FileNotFoundError:
        messagebox.showinfo("Histórico de Conversas", "Nenhum histórico encontrado.")

def start_voice_recognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Gravação", "Diga algo!")
        audio = recognizer.listen(source)
        try:
            user_message = recognizer.recognize_google(audio)
            entry_message.delete(0, tk.END)
            entry_message.insert(0, user_message)
            send_message()
        except sr.UnknownValueError:
            messagebox.showinfo("Erro", "Não consegui entender o áudio.")
        except sr.RequestError:
            messagebox.showinfo("Erro", "Erro ao conectar com o serviço de reconhecimento de voz.")

# Configurações iniciais
config = load_config()

# Configurações da janela principal
root = tk.Tk()
root.title("SOF.IA Assistente Virtual")

# Menu de Configurações
menu = tk.Menu(root)
root.config(menu=menu)

settings_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Configurações", menu=settings_menu)
settings_menu.add_command(label="Mudar Tema", command=change_theme)
settings_menu.add_command(label="Manual de Uso", command=show_help)
settings_menu.add_command(label="Histórico de Conversas", command=show_history)
settings_menu.add_command(label="Reconhecimento de Voz", command=start_voice_recognition)

# Log de conversas
chat_log = tk.Text(root, state="normal", height=20, width=50)
chat_log.pack(pady=10)

# Campo de entrada de mensagens
entry_message = tk.Entry(root, width=40)
entry_message.pack(pady=10)
entry_message.bind("<Return>", send_message)

# Botão de enviar
send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(pady=10)

# Aplicar o tema configurado
apply_theme()

root.mainloop()
