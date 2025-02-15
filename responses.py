import json
import random
import webbrowser

def load_responses():
    try:
        with open("responses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "greetings": ["Olá! Como posso ajudar você hoje?", "Oi! O que você precisa?", "Olá! Em que posso ser útil?"],
            "wellbeing": ["Estou bem, obrigado por perguntar! E você?", "Tudo ótimo por aqui! E com você?", "Estou bem! Como você está?"],
            "name": ["Eu sou a SOF.IA, seu assistente virtual.", "Meu nome é SOF.IA.", "Pode me chamar de SOF.IA."],
            "weather": ["Não tenho acesso ao tempo no momento.", "Infelizmente, não posso informar sobre o tempo agora."],
            "help": ["Estou aqui para ajudar. O que você precisa?", "Como posso te ajudar hoje?"],
            "farewell": ["Até logo! Se precisar de mais alguma coisa, é só chamar.", "Tchau! Tenha um ótimo dia."],
            "project": ["Você está trabalhando no projeto SOF.IA. Como posso ajudar?"],
            "default": ["Desculpe, não compreendi a sua pergunta. Pode reformular?", "Não entendi. Pode explicar de outra forma?"]
        }

def get_response(user_message):
    responses = load_responses()
    user_message = user_message.lower()

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
    elif "pesquisar sobre" in user_message:
        query = user_message.replace("pesquisar sobre", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Pesquisando sobre: {query}"
    elif "calcular" in user_message:
        from utils import calcular_expressao
        return calcular_expressao(user_message)
    else:
        return random.choice(responses.get("default", []))
