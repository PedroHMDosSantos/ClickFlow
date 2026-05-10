import pyautogui
import time
import tkinter as tk
from tkinter import filedialog
import threading
import keyboard
import os
import sys
import json

# ===== CONFIG =====
BG = "#1e1e1e"
FG = "#ffffff"
BTN = "#2d2d2d"
ACCENT = "#4CAF50"
HINT = "#aaaaaa"

pontos = []
rodando = False


# ===== PATH DINÂMICO =====
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    return os.path.join(base_path, relative_path)


# ===== TOOLTIP =====
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None

        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 35

        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        self.tip.configure(bg="#2b2b2b")

        label = tk.Label(
            self.tip,
            text=self.text,
            justify="left",
            bg="#2b2b2b",
            fg=FG,
            relief="solid",
            bd=1,
            padx=10,
            pady=6,
            wraplength=260,
            font=("Segoe UI", 9)
        )
        label.pack()

    def hide_tip(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


# ===== HOVER ENTRY =====
def hover_entry(widget):
    def entrar(e):
        widget.config(
            bg="#353535",
            highlightbackground=ACCENT,
            highlightcolor=ACCENT,
            highlightthickness=1
        )

    def sair(e):
        widget.config(
            bg="#2b2b2b",
            highlightthickness=0
        )

    widget.bind("<Enter>", entrar)
    widget.bind("<Leave>", sair)


# ===== LOG =====
def log(msg):
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)


# ===== FUNÇÕES =====
def adicionar_ponto():
    log("Capturando ponto em 3s...")
    root.update()
    time.sleep(3)

    pos = pyautogui.position()
    pontos.append((pos.x, pos.y))

    log(f"Ponto adicionado: {pos}")


def remover_ultimo():
    if pontos:
        removido = pontos.pop()
        log(f"Removido: {removido}")
    else:
        log("Nenhum ponto para remover")


# ===== SALVAR COMO =====
def salvar_config():
    try:
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivo JSON", "*.json")],
            title="Salvar configuração"
        )

        if not arquivo:
            return

        dados = {
            "delay": entry_delay.get(),
            "ciclos": entry_ciclos.get(),
            "pontos": pontos
        }

        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)

        log("Configuração salva com sucesso!")

    except Exception as e:
        log(f"Erro ao salvar: {e}")


# ===== CARREGAR =====
def carregar_config():
    global pontos

    try:
        arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivo JSON", "*.json")],
            title="Carregar configuração"
        )

        if not arquivo:
            return

        with open(arquivo, "r") as f:
            dados = json.load(f)

        pontos = [tuple(p) for p in dados["pontos"]]

        entry_delay.delete(0, tk.END)
        entry_delay.insert(0, dados["delay"])

        entry_ciclos.delete(0, tk.END)
        entry_ciclos.insert(0, dados["ciclos"])

        log("Configuração carregada com sucesso!")
        log(f"{len(pontos)} ponto(s) restaurado(s).")

    except Exception as e:
        log(f"Erro ao carregar: {e}")


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
    status_label.config(text="● Parado (F6 para iniciar)", fg=HINT)
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


# ===== UI =====
root = tk.Tk()
root.title("ClickFlow")
root.geometry("420x560")
root.configure(bg=BG)

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
        pady=6,
        cursor="hand2"
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

hover_entry(entry_delay)
hover_entry(entry_ciclos)

ToolTip(
    entry_delay,
    "Define o intervalo entre os cliques executados em cada ponto registrado.\nValores menores = cliques mais rápidos."
)

ToolTip(
    entry_ciclos,
    "Quantas vezes repetir todos os pontos salvos.\nDeixe vazio para modo infinito."
)


# ===== TEXTO =====
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


# ===== SAVE / LOAD =====
save_frame = tk.Frame(frame, bg=BG)
save_frame.pack(fill="x", pady=8)

btn(save_frame, "Salvar Config", salvar_config).grid(row=0, column=0, sticky="we", padx=2)
btn(save_frame, "Carregar Config", carregar_config).grid(row=0, column=1, sticky="we", padx=2)

save_frame.columnconfigure((0, 1), weight=1)


# ===== STATUS =====
status_label = tk.Label(
    frame,
    text="● Parado (F6 para iniciar)",
    bg=BG,
    fg=HINT,
    font=("Segoe UI", 10, "bold")
)
status_label.pack(anchor="w", pady=10)


# ===== LOG =====
log_text = tk.Text(frame, height=8, bg="#2b2b2b", fg=FG, relief="flat")
log_text.pack(fill="both", expand=True)


# ===== HOTKEY =====
keyboard.add_hotkey("F6", toggle_hotkey)

root.mainloop()