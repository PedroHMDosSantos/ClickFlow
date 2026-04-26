import pyautogui
import time
import tkinter as tk
from tkinter import ttk
import threading
import keyboard

# ===== CONFIG DARK MODE =====
BG = "#ffffff"
FG = "#000000"
BTN = "#ffffff"
ACCENT = "#4CAF50"

# ===== VARIÁVEIS =====
ponto1 = None
ponto2 = None
rodando = False

# ===== FUNÇÕES =====
def capturar_ponto1():
    global ponto1
    log("Capturando ponto 1 em 3s...")
    root.update()
    time.sleep(3)
    ponto1 = pyautogui.position()
    log(f"Ponto 1: {ponto1}")

def capturar_ponto2():
    global ponto2
    log("Capturando ponto 2 em 3s...")
    root.update()
    time.sleep(3)
    ponto2 = pyautogui.position()
    log(f"Ponto 2: {ponto2}")

def loop_cliques():
    global rodando

    try:
        z = int(entry_vezes.get())
        delay = float(entry_delay.get())
    except:
        log("Valores inválidos!")
        rodando = False
        return

    progresso["maximum"] = z
    progresso["value"] = 0

    for i in range(z):
        if not rodando:
            log("Parado!")
            break

        pyautogui.click(ponto1)
        time.sleep(delay)
        pyautogui.click(ponto2)
        time.sleep(delay)

        progresso["value"] = i + 1
        root.update_idletasks()

    rodando = False
    log("Concluído!")

def iniciar():
    global rodando

    if not ponto1 or not ponto2:
        log("Defina os dois pontos primeiro!")
        return

    if rodando:
        return

    rodando = True
    log("Iniciado (F6 para parar)")

    thread = threading.Thread(target=loop_cliques)
    thread.start()

def parar():
    global rodando
    rodando = False

def toggle_hotkey():
    global rodando
    if rodando:
        parar()
    else:
        iniciar()

def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)

# ===== UI =====
root = tk.Tk()
root.title("Clique Automático")
root.geometry("420x420")
root.configure(bg=BG)

frame = tk.Frame(root, bg=BG)
frame.pack(anchor="w", padx=15, pady=10)

def styled_label(text):
    return tk.Label(frame, text=text, bg=BG, fg=FG, anchor="w")

def styled_entry():
    return tk.Entry(frame, bg="#998686", fg=FG, insertbackground=FG, relief="flat")

def styled_button(text, cmd):
    return tk.Button(
        frame,
        text=text,
        command=cmd,
        bg="#998686",
        fg=FG,
        activebackground=ACCENT,
        activeforeground="#000",
        relief="flat",
        padx=10,
        pady=5
    )

styled_label("Quantidade de cliques:").pack(anchor="w")
entry_vezes = styled_entry()
entry_vezes.pack(anchor="w", fill="x", pady=5)

styled_label("Delay (segundos):").pack(anchor="w")
entry_delay = styled_entry()
entry_delay.pack(anchor="w", fill="x", pady=5)

styled_button("Capturar Ponto 1 (3s)", capturar_ponto1).pack(anchor="w", pady=5)
styled_button("Capturar Ponto 2 (3s)", capturar_ponto2).pack(anchor="w", pady=5)
styled_button("Iniciar", iniciar).pack(anchor="w", pady=10)

# Progress bar
style = ttk.Style()
style.theme_use("default")
style.configure("TProgressbar",
                troughcolor="#998686",
                background=ACCENT,
                thickness=10)

progresso = ttk.Progressbar(frame, length=350, style="TProgressbar")
progresso.pack(anchor="w", pady=10)

# Log
log_text = tk.Text(
    frame,
    height=8,
    bg="#998686",
    fg=FG,
    insertbackground=FG,
    relief="flat"
)
log_text.pack(anchor="w", fill="both")

# ===== HOTKEY F6 =====
keyboard.add_hotkey("F6", toggle_hotkey)

log("Pressione F6 para iniciar/parar")

root.mainloop()