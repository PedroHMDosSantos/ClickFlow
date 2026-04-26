import pyautogui
import time
import tkinter as tk
import threading
import keyboard
import os
import sys

# ===== CONFIG =====
BG = "#1e1e1e"
FG = "#ffffff"
BTN = "#2d2d2d"
ACCENT = "#4CAF50"
HINT = "#aaaaaa"

pontos = []
rodando = False


# ===== PATH DINÂMICO (CORREÇÃO DO ÍCONE) =====
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # quando vira .exe
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)


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

        ciclos = float("inf") if ciclos_txt == "" else int(ciclos_txt)

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
    status_label.config(text="● Parado (F6 para iniciar)", fg="#aaaaaa")
    log("Concluído!")


def iniciar():
    global rodando

    if not pontos:
        log("Adicione pontos primeiro!")
        return

    if rodando:
        return

    rodando = True
    status_label.config(text="● Rodando (F6 para parar)", fg=ACCENT)
    log("Iniciado")
    threading.Thread(target=loop_cliques, daemon=True).start()


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
root.title("ClickFlow")
root.geometry("420x520")
root.configure(bg=BG)

# ✔ ÍCONE CORRIGIDO (AGORA FUNCIONA EM QUALQUER PC)
root.iconbitmap(resource_path("assets/click.ico"))

frame = tk.Frame(root, bg=BG)
frame.pack(fill="both", expand=True, padx=15, pady=10)


def btn(parent, text, cmd):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=BTN,
        fg=FG,
        activebackground=ACCENT,
        relief="flat",
        padx=10,
        pady=6
    )


# ===== CONFIG =====
config_frame = tk.Frame(frame, bg=BG)
config_frame.pack(fill="x", pady=5)

tk.Label(config_frame, text="Delay (s)", bg=BG, fg=FG).grid(row=0, column=0, sticky="w")
entry_delay = tk.Entry(config_frame, bg="#2b2b2b", fg=FG, insertbackground=FG)
entry_delay.grid(row=1, column=0, sticky="we", padx=(0, 10))

tk.Label(config_frame, text="Ciclos", bg=BG, fg=FG).grid(row=0, column=1, sticky="w")
entry_ciclos = tk.Entry(config_frame, bg="#2b2b2b", fg=FG, insertbackground=FG)
entry_ciclos.grid(row=1, column=1, sticky="we")

config_frame.columnconfigure(0, weight=1)
config_frame.columnconfigure(1, weight=1)


# ===== DICA =====
tk.Label(
    frame,
    text="Posicione o mouse no ponto desejado e aguarde 3 segundos após clicar para registrar cada ponto.",
    bg=BG,
    fg=HINT,
    wraplength=380,
    justify="left"
).pack(anchor="w", pady=(10, 10))


# ===== BOTÕES =====
btn_frame = tk.Frame(frame, bg=BG)
btn_frame.pack(fill="x", pady=5)

btn(btn_frame, "Adicionar Ponto", adicionar_ponto).grid(row=0, column=0, sticky="we", padx=2)
btn(btn_frame, "Remover Último", remover_ultimo).grid(row=0, column=1, sticky="we", padx=2)
btn(btn_frame, "Iniciar", iniciar).grid(row=0, column=2, sticky="we", padx=2)

btn_frame.columnconfigure((0, 1, 2), weight=1)


# ===== STATUS =====
status_label = tk.Label(
    frame,
    text="● Parado (F6 para iniciar)",
    bg=BG,
    fg="#aaaaaa",
    font=("Segoe UI", 10, "bold")
)
status_label.pack(anchor="w", pady=10)


# ===== LOG =====
log_text = tk.Text(frame, height=8, bg="#2b2b2b", fg=FG, relief="flat")
log_text.pack(fill="both", expand=True)


# ===== HOTKEY =====
keyboard.add_hotkey("F6", toggle_hotkey)

root.mainloop()