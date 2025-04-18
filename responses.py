import random
import webbrowser
import datetime
import pyttsx3
import os
import json
import time
from datetime import datetime
from responses_data import responses_dict
from commands import commands
from config import load_config

# Configurações iniciais
engine = pyttsx3.init()
config = load_config()

# Aplica confiqurações ao engine
if config["voice_id"]:
    engine.setProperty('voice', config["voice_id"])
engine.setProperty("rate", config.get("rate", 150))

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()

        if config.get("save_audio", True):
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pasta = os.path.join("tpf_gravacoes", "falas")
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, f"falas_{now}.mp3")
            engine.save_to_file(text, caminho)
            engine.runAndWait()

    except Exception as e:
        print(f"Erro ao falar: {e}")

# Carrega respostas do dicionário JSON
def load_responses():
    try:
        with open("responses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "greetings": ["Olá! Como posso ajudar?", "Oi! O que você precisa?", "E aí! Em que posso ser útil?"],
            "wellbeing": ["Estou bem! E você?", "Tudo ótimo! E contigo?", "Bem por aqui! E você?"],
            "name": ["Eu sou a SOF.IA!", "Meu nome é SOF.IA!", "Pode me chamar de SOF.IA."],
            "weather": ["Não tenho acesso ao clima no momento.", "Infelizmente, não posso ver o tempo agora."],
            "help": ["Estou aqui para ajudar! O que você precisa?", "Como posso te ajudar hoje?"],
            "farewell": ["Até logo!", "Tchau! Volte sempre!", "Adeus!"],
            "project": ["O projeto SOF.IA está progredindo! Como posso ajudar?", "Você está trabalhando na SOF.IA, certo?"],
            "default": ["Desculpe, não compreendi. Pode reformular?", "Não entendi, pode repetir?"]
        }
    
# time
def get_time():
    now = datetime.now()
    now_format = now.strftime("%H:%M")
    return f"Agora são {now_format} horas."

# Detecta o comando baseado no dicionário
def detect_command(user_message):
    user_message = user_message.lower()
    
    for category, keywords in commands.items():
        if any(keyword in user_message for keyword in keywords):
            return category
    
    return "default"

# Processa a resposta para um comando detectado
def get_response(user_message):
    responses = load_responses()
    command = detect_command(user_message)

    if command == "search":
        query = user_message.replace("pesquisar sobre", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Pesquisando sobre: {query}"

    elif command == "calculate":
        try:
            expression = user_message.replace("calcular", "").strip()
            result = eval(expression, {"__builtins__": None}, {})
            return f"O resultado é: {result}"
        except:
            return "Não consegui calcular a expressão."
        
    elif command == "time":
        return get_time()

    return random.choice(responses.get(command, responses["default"]))

# Texto para fala
def speak_response(response):
    speak(response)

# coisas a mais
if __name__ == "__main__":
    pass