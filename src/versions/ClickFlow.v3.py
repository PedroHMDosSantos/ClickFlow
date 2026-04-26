import pyautogui
import time
import tkinter as tk
import threading
import keyboard

# ===== CONFIG =====
BG = "#1e1e1e"
FG = "#ffffff"
BTN = "#2d2d2d"
ACCENT = "#4CAF50"
HINT = "#aaaaaa"  # cor da dica

pontos = []
rodando = False

# ===== FUNÇÕES =====
def adicionar_ponto():
    log("Capturando ponto em 3s...")
    root.update()
    time.sleep(3)
    pos = pyautogui.position()
    pontos.append(pos)
    log(f"Ponto adicionado: {pos}")

def remover_ultimo():
    if pontos:
        removido = pontos.pop()
        log(f"Removido: {removido}")
    else:
        log("Nenhum ponto para remover")

def loop_cliques():
    global rodando
    try:
        delay = float(entry_delay.get())
        ciclos_txt = entry_ciclos.get()

        if ciclos_txt == "":
            ciclos = float("inf")
        else:
            ciclos = int(ciclos_txt)

    except:
        log("Valores inválidos!")
        rodando = False
        return

    i = 0

    while i < ciclos and rodando:
        for p in pontos:
            if not rodando:
                break
            pyautogui.click(p)
            time.sleep(delay)

        i += 1

    rodando = False
    status_label.config(text="Status: Parado (F6 para iniciar)", fg="#aaaaaa")
    log("Concluído!")

def iniciar():
    global rodando
    if not pontos:
        log("Adicione pontos primeiro!")
        return

    if rodando:
        return

    rodando = True
    status_label.config(text="Status: Rodando (F6 para parar)", fg=ACCENT)
    log("Iniciado")
    threading.Thread(target=loop_cliques).start()

def parar():
    global rodando
    rodando = False

def toggle_hotkey():
    if rodando:
        parar()
    else:
        iniciar()

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)

# ===== UI =====
root = tk.Tk()
root.title("Auto Click PRO")
root.geometry("420x450")
root.configure(bg=BG)

frame = tk.Frame(root, bg=BG)
frame.pack(anchor="w", padx=15, pady=10)

def btn(text, cmd):
    return tk.Button(frame, text=text, command=cmd, bg=BTN, fg=FG,
                     activebackground=ACCENT, relief="flat", padx=8, pady=4)

# Inputs
tk.Label(frame, text="Delay (segundos):", bg=BG, fg=FG).pack(anchor="w")
entry_delay = tk.Entry(frame, bg="#2b2b2b", fg=FG, insertbackground=FG)
entry_delay.pack(anchor="w", fill="x", pady=5)

tk.Label(frame, text="Quantidade de ciclos (vazio = infinito):", bg=BG, fg=FG).pack(anchor="w")
entry_ciclos = tk.Entry(frame, bg="#2b2b2b", fg=FG, insertbackground=FG)
entry_ciclos.pack(anchor="w", fill="x", pady=5)

# Menssagem de dica de como usar o programa
tk.Label(
    frame,
    text="Posicione o mouse no ponto desejado e aguarde 3 segundos após clicar para registrar cada ponto.",
    bg=BG,
    fg=HINT,
    wraplength=380,
    justify="left"
).pack(anchor="w", pady=(10, 5))

# Botões
btn("Adicionar Ponto (3s)", adicionar_ponto).pack(anchor="w", pady=3)
btn("Remover Último", remover_ultimo).pack(anchor="w", pady=3)
btn("Iniciar", iniciar).pack(anchor="w", pady=8)

# Status
status_label = tk.Label(
    frame,
    text="Status: Parado (F6 para iniciar)",
    bg=BG,
    fg="#aaaaaa"
)
status_label.pack(anchor="w", pady=10)

# Log
log_text = tk.Text(frame, height=8, bg="#2b2b2b", fg=FG)
log_text.pack(anchor="w", fill="both")

# Hotkey
keyboard.add_hotkey("F6", toggle_hotkey)

root.mainloop()