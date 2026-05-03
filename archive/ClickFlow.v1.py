import pyautogui
import time
import tkinter as tk 
from tkinter import ttk

print("Coloque o mouse no PRIMEIRO ponto e pressione ENTER...")
input()
x1, y1 = pyautogui.position()
print(f"Primeiro ponto capturado: ({x1}, {y1})")

print("Coloque o mouse no SEGUNDO ponto e pressione ENTER...")
input()
x2, y2 = pyautogui.position()
print(f"Segundo ponto capturado: ({x2}, {y2})")

z = int(input("Quantas vezes deseja alternar os cliques? "))
delay = float(input("Tempo de espera entre cliques (segundos): "))

print("Prepare-se! Você tem 3 segundos...")
time.sleep(3)


for i in range(z):
    pyautogui.click(x1, y1)
    time.sleep(delay)
    pyautogui.click(x2, y2)
    time.sleep(delay)

print("Concluído!")


#Fiz só de bobeira pra tirar umas musicas rapidamente no spotfy kkkkkkkkkkkkkkkkkkkkkkk