import os
import time
import threading
import sqlite3
import json
import curses
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Configuração do modelo Qwen
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
try:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
except Exception as e:
    print(f"Erro ao carregar o modelo '{model_name}': {e}")
    exit(1)

# Variáveis globais
chat_history = []
history_file = "history_log.json"
max_messages = 5  # Número de mensagens antes de salvar no arquivo

def get_answer_from_model(question):
    global chat_history
    system_prompt = {
        "role": "system",
        "content": "Você é SOF.ia, um assistente virtual avançado e amigável, focado em ajudar desenvolvledores a resolver problema técnicos, gerar ideias criativas e facilitar projetos de programação. Responda de forma clara e adaptada ás necessidades do usuário."
    }
    user_prompt = {"role": "user", "content": question}
    messages = [system_prompt] + [{"role": "assistant", "content": msg} for msg in chat_history[-5:]] + [user_prompt]

    try:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        generated_ids = model.generate(**model_inputs, max_new_tokens=512)
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response.strip()
    except Exception as e:
        return f"Erro ao processar a pergunta: {str(e)}"

def save_chat_history():
    global chat_history
    if chat_history:
        if os.path.exists(history_file):
            with open(history_file, "r") as file:
                existing_history = json.load(file)
        else:
            existing_history = []

        existing_history.extend(chat_history)

        with open(history_file, "w") as file:
            json.dump(existing_history, file, indent=4)

        chat_history = []

def periodic_save(interval=60):
    while True:
        time.sleep(interval)
        save_chat_history()

def curses_interface(stdscr):
    global chat_history

    # Configurar a interface
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Divisões de tela
    input_win = curses.newwin(3, width, height - 3, 0)
    chat_win = curses.newwin(height - 4, width, 0, 0)
    input_win.box()
    chat_win.scrollok(True)

    # Pré-contexto
    pre_context = (
        "Bem-vindo ao SOF.ia - Assistente Virtual\n"
        "Use Ctrl+G para ver o contexto inicial novamente.\n"
        "Use Ctrl+Q para sair do programa.\n"
        "Digite sua mensagem abaixo e pressione Enter."
    )
    chat_win.addstr(pre_context + "\n")
    chat_win.refresh()

    user_input = ""



    while True:
        input_win.clear()
        input_win.box()
        input_win.addstr(1, 1, f"Você: {user_input}")
        input_win.refresh()

        key = stdscr.getch()

        # Sair com Ctrl+Q
        if key == 17:  # Ctrl+Q
            save_chat_history()
            break

        # Mostrar pré-contexto com Ctrl+G
        elif key == 7:  # Ctrl+G
            chat_win.addstr(pre_context + "\n")
            chat_win.refresh()

        # Enter para enviar mensagem
        elif key == 10:  # Enter
            if user_input.strip():
                chat_win.addstr(f"Você: {user_input.strip()}\n")
                response = get_answer_from_model(user_input.strip())
                chat_win.addstr(f"SOF.IA: {response}\n")
                chat_win.refresh()

                chat_history.append(f"Você: {user_input.strip()}")
                chat_history.append(f"SOF.IA: {response}")
                user_input = ""

        # Backspace
        elif key == 127 or key == curses.KEY_BACKSPACE:
            user_input = user_input[:-1]

        # Adicionar caracteres ao input
        elif 32 <= key <= 126:
            user_input += chr(key)

if __name__ == "__main__":
    threading.Thread(target=periodic_save, daemon=True).start()
    curses.wrapper(curses_interface)

