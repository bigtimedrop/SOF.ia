import curses
import time
import sqlite3
from transformers import AutoModelForCausalLM, AutoTokenizer

# Variáveis globais
model = None
tokenizer = None

def connect_db():
    try:
        conn = sqlite3.connect("chatbot.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS qa (pergunta TEXT PRIMARY KEY, resposta TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")
        conn.commit()
        conn.close()
        return "Banco de dados conectado."
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {e}"

def load_model(stdscr):
    global model, tokenizer
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    try:
        # Atualiza a interface com mensagem de carregamento
        stdscr.addstr(3, 10, "Carregando modelo...")
        stdscr.refresh()
        time.sleep(1)  # Simulação de espera (para visualização)

        # Carregando modelo e tokenizer
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        return "Modelo carregado com sucesso."
    except Exception as e:
        return f"Erro ao carregar o modelo: {e}"

def loading_screen(stdscr):
    # Esconde o cursor
    curses.curs_set(0)
    stdscr.clear()

    # Mensagem inicial
    stdscr.addstr(1, 10, "Iniciando SOF.ia...")
    stdscr.refresh()
    time.sleep(1)

    # Etapa 1: Conectar ao banco de dados
    db_status = connect_db()
    stdscr.addstr(3, 10, db_status)
    stdscr.refresh()
    time.sleep(1)

    # Etapa 2: Carregar o modelo
    model_status = load_model(stdscr)
    stdscr.addstr(5, 10, model_status)
    stdscr.refresh()
    time.sleep(1)

    # Barra de progresso final
    loading_message = "Concluindo inicialização..."
    progress_bar_length = 20
    stdscr.addstr(7, 10, loading_message)
    for i in range(progress_bar_length + 1):
        stdscr.addstr(9, 10, f"[{'#' * i}{'.' * (progress_bar_length - i)}]")
        stdscr.refresh()
        time.sleep(0.1)

    # Mensagem de conclusão
    stdscr.addstr(11, 10, "SOF.ia está pronto! Pressione qualquer tecla para continuar.")
    stdscr.refresh()
    stdscr.getch()  # Espera o usuário pressionar uma tecla

def main_screen(stdscr):
    # Tela principal de interação
    stdscr.clear()
    stdscr.addstr(0, 0, "Bem-vindo ao SOF.ia!")
    stdscr.addstr(1, 0, "Digite sua mensagem abaixo:")
    stdscr.refresh()

    # Entrada do usuário
    while True:
        stdscr.addstr(3, 0, "Você: ")
        user_message = stdscr.getstr(3, 6, 60).decode("utf-8").strip()

        if user_message.lower() == "sair":
            stdscr.addstr(5, 0, "Sessão encerrada. Até logo!")
            stdscr.refresh()
            time.sleep(2)
            break

        # Gerar resposta (simulação para exemplo)
        response = f"Você disse: {user_message}"
        stdscr.addstr(5, 0, f"SOF.ia: {response}")
        stdscr.refresh()

def main():
    curses.wrapper(loading_screen)  # Tela de carregamento
    curses.wrapper(main_screen)    # Tela principal

if __name__ == "__main__":
    main()

