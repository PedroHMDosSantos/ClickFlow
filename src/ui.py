import tkinter as tk
import keyboard

from theme import *
from helpers import resource_path
from tooltips import ToolTip
from clicker import *
from storage import *


def iniciar_app():
    root = tk.Tk()
    root.title("ClickFlow")
    root.geometry("420x560")
    root.configure(bg=BG)
    root.iconbitmap(resource_path("assets/click.ico"))

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True, padx=12, pady=10)

    # =========================
    # LOG
    # =========================
    def log(msg):
        log_text.insert(tk.END, msg + "\n")
        log_text.see(tk.END)

    # =========================
    # STATUS
    # =========================
    def atualizar_status(on):
        if on:
            status.config(
                text="● Rodando (F6 para parar)",
                fg=ACCENT
            )
        else:
            status.config(
                text="● Parado (F6 para iniciar)",
                fg=HINT
            )

    # =========================
    # START
    # =========================
    def start():
        try:
            delay = float(entry_delay.get())

            txt = entry_ciclos.get()
            ciclos = float("inf") if txt == "" else int(txt)

            iniciar(delay, ciclos, log, atualizar_status)

        except:
            log("Valores inválidos!")

    # =========================
    # TOGGLE F6
    # =========================
    def toggle():
        if rodando:
            parar()
            atualizar_status(False)
        else:
            start()

    # =========================
    # SALVAR
    # =========================
    def salvar():
        ok = salvar_config(
            entry_delay.get(),
            entry_ciclos.get(),
            pontos
        )

        if ok:
            log("Configuração salva!")

    # =========================
    # CARREGAR
    # =========================
    def carregar():
        dados = carregar_config()

        if not dados:
            return

        pontos.clear()
        pontos.extend([tuple(p) for p in dados["pontos"]])

        entry_delay.delete(0, tk.END)
        entry_delay.insert(0, dados["delay"])

        entry_ciclos.delete(0, tk.END)
        entry_ciclos.insert(0, dados["ciclos"])

        log("Configuração carregada!")

    # =========================
    # BOTÃO BONITO
    # =========================
    def btn(parent, txt, cmd):
        return tk.Button(
            parent,
            text=txt,
            command=cmd,
            bg=BTN,
            fg=FG,
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=10,
            pady=8,
            font=("Segoe UI", 10),
            cursor="hand2"
        )

    # =========================
    # CONFIG
    # =========================
    config = tk.Frame(frame, bg=BG)
    config.pack(fill="x", pady=(0, 10))

    tk.Label(
        config,
        text="Delay (s)",
        bg=BG,
        fg=FG,
        font=("Segoe UI", 9)
    ).grid(row=0, column=0, sticky="w")

    tk.Label(
        config,
        text="Ciclos",
        bg=BG,
        fg=FG,
        font=("Segoe UI", 9)
    ).grid(row=0, column=1, sticky="w")

    entry_delay = tk.Entry(
        config,
        bg=ENTRY_BG,
        fg=FG,
        insertbackground=FG,
        relief="flat",
        font=("Segoe UI", 10)
    )

    entry_ciclos = tk.Entry(
        config,
        bg=ENTRY_BG,
        fg=FG,
        insertbackground=FG,
        relief="flat",
        font=("Segoe UI", 10)
    )

    entry_delay.grid(row=1, column=0, sticky="we", padx=(0, 10), ipady=4)
    entry_ciclos.grid(row=1, column=1, sticky="we", ipady=4)

    config.columnconfigure(0, weight=1)
    config.columnconfigure(1, weight=1)

    # =========================
    # TOOLTIPS
    # =========================
    ToolTip(
        entry_delay,
        "Define o intervalo entre os cliques executados em cada ponto registrado.\nValores menores = cliques mais rápidos."
    )

    ToolTip(
        entry_ciclos,
        "Quantas vezes repetir todos os pontos salvos.\nDeixe vazio para modo infinito."
    )

    # =========================
    # TEXTO INFO
    # =========================
    tk.Label(
        frame,
        text="Posicione o mouse no ponto desejado e aguarde 3 segundos após clicar para registrar cada ponto.",
        bg=BG,
        fg=HINT,
        wraplength=380,
        justify="left",
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 12))

    # =========================
    # BOTÕES AÇÃO
    # =========================
    area = tk.Frame(frame, bg=BG)
    area.pack(fill="x", pady=(0, 10))

    btn(area, "Adicionar Ponto",
        lambda: adicionar_ponto(log, root)
        ).grid(row=0, column=0, sticky="we", padx=2)

    btn(area, "Remover Último",
        lambda: remover_ultimo(log)
        ).grid(row=0, column=1, sticky="we", padx=2)

    btn(area, "Iniciar",
        start
        ).grid(row=0, column=2, sticky="we", padx=2)

    area.columnconfigure((0, 1, 2), weight=1)

    # =========================
    # SAVE LOAD
    # =========================
    save = tk.Frame(frame, bg=BG)
    save.pack(fill="x", pady=(0, 12))

    btn(save, "Salvar Config", salvar).grid(
        row=0, column=0, sticky="we", padx=(0, 2)
    )

    btn(save, "Carregar Config", carregar).grid(
        row=0, column=1, sticky="we", padx=(2, 0)
    )

    save.columnconfigure((0, 1), weight=1)

    # =========================
    # STATUS
    # =========================
    status = tk.Label(
        frame,
        text="● Parado (F6 para iniciar)",
        bg=BG,
        fg=HINT,
        font=("Segoe UI", 10, "bold")
    )
    status.pack(anchor="w", pady=(0, 10))

    # =========================
    # LOG
    # =========================
    log_text = tk.Text(
        frame,
        height=10,
        bg=ENTRY_BG,
        fg=FG,
        relief="flat",
        bd=0,
        font=("Consolas", 10)
    )
    log_text.pack(fill="both", expand=True)

    # =========================
    # HOTKEY
    # =========================
    keyboard.add_hotkey("F6", toggle)

    root.mainloop()