import os

HISTORY_FILE = "history.txt"

def save_to_history(user_message, response):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"Você: {user_message}\nSOF.IA: {response}\n\n")

def calcular_expressao(user_message):
    try:
        expression = user_message.replace("calcular", "").strip()
        result = eval(expression, {"__builtins__": None}, {})
        return f"O resultado é: {result}"
    except Exception:
        return "Desculpe, não consegui calcular a expressão."
