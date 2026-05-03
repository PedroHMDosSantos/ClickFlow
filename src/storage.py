import json
from tkinter import filedialog

def salvar_config(delay, ciclos, pontos):
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON", "*.json")],
        title="Salvar Configuração"
    )

    if not arquivo:
        return False

    dados = {
        "delay": delay,
        "ciclos": ciclos,
        "pontos": pontos
    }

    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

    return True


def carregar_config():
    arquivo = filedialog.askopenfilename(
        filetypes=[("JSON", "*.json")],
        title="Carregar Configuração"
    )

    if not arquivo:
        return None

    with open(arquivo, "r") as f:
        return json.load(f)