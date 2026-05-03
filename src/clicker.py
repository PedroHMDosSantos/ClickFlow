import pyautogui
import time
import threading

pontos = []
rodando = False

def adicionar_ponto(log, root):
    log("Capturando ponto em 3s...")
    root.update()
    time.sleep(3)

    pos = pyautogui.position()
    pontos.append((pos.x, pos.y))
    log(f"Ponto adicionado: {pos}")

def remover_ultimo(log):
    if pontos:
        log(f"Removido: {pontos.pop()}")
    else:
        log("Nenhum ponto para remover")

def parar():
    global rodando
    rodando = False

def iniciar(delay, ciclos, log, atualizar_status):
    global rodando

    if not pontos:
        log("Adicione pontos primeiro!")
        return

    if rodando:
        return

    rodando = True
    atualizar_status(True)

    threading.Thread(
        target=loop,
        args=(delay, ciclos, log, atualizar_status),
        daemon=True
    ).start()

def loop(delay, ciclos, log, atualizar_status):
    global rodando

    i = 0

    while i < ciclos and rodando:
        for p in pontos:
            if not rodando:
                break

            pyautogui.click(p)
            time.sleep(delay)

        i += 1

    rodando = False
    atualizar_status(False)
    log("Concluído!")