import os
import time
import threading
import sqlite3
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

# Variáveis globais
chat_history = []
history_file = "history_log.json"
max_messages = 5  # Número de mensagens antes de salvar no arquivo

# Carregar modelo Gwen 0.5
model_name = "Qwen/Qwen2.5-0.5B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def get_answer_from_model(question):
    global chat_history
    recent_context = " ".join(chat_history[-5:])  # Pega as últimas 5 mensagens do histórico
    base_context = "Você é um assistente virtual chamado SOF.ai, com foco em criação de projetos de programação."
    combined_context = base_context + " " + recent_context

    try:
        input_text = f"Contexto: {combined_context}\nPergunta: {question}\nResposta:"
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=150)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Resposta:")[-1].strip()
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}"

def get_answer_from_db(question):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT resposta FROM qa WHERE pergunta = ?", (question,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_chat_history():
    global chat_history
    if chat_history:  # Apenas salva se houver mensagens
        if os.path.exists(history_file):
            with open(history_file, "r") as file:
                existing_history = json.load(file)
        else:
            existing_history = []

        existing_history.extend(chat_history)

        with open(history_file, "w") as file:
            json.dump(existing_history, file, indent=4)

        chat_history = []  # Limpa a memória após salvar

def periodic_save(interval=60):
    while True:
        time.sleep(interval)  # Espera o intervalo especificado
        save_chat_history()

def connect_db():
    conn = sqlite3.connect("chatbot.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS qa (pergunta TEXT PRIMARY KEY, resposta TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")
    conn.commit()
    return conn

def get_memory(key):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT value FROM memory WHERE key = ?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_memory(key, value):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_response(user_message):
    # Verificar se a mensagem é para configurar memória
    if user_message.lower().startswith("meu nome é"):
        name = user_message.split("é", 1)[1].strip()
        save_memory("user_name", name)
        return f"Entendido, vou lembrar que seu nome é {name}."

    # Recuperar nome do usuário, se disponível
    user_name = get_memory("user_name")
    if user_name:
        user_message = f"{user_name} diz: {user_message}"

    # Consultar no banco de dados
    response = get_answer_from_db(user_message)

    if response is None:
        # Consultar o modelo se a resposta não estiver no banco
        response = get_answer_from_model(user_message)
        save_answer_to_db(user_message, response)

    return response

def save_answer_to_db(question, answer):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO qa (pergunta, resposta) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def main():
    print("Bem-vindo ao SOF.IA CLI - Assistente Virtual")
    print("Digite 'sair' para encerrar a sessão.")

    while True:
        user_message = input("Você: ").strip()
        if user_message.lower() == "sair":
            save_chat_history()
            print("Sessão encerrada. Histórico salvo.")
            break

        response = get_response(user_message)
        print(f"SOF.IA: {response}")

        chat_history.append(f"Você: {user_message}")
        chat_history.append(f"SOF.IA: {response}")

# Iniciar a thread para salvamento periódico
threading.Thread(target=periodic_save, daemon=True).start()

if __name__ == "__main__":
    main()
