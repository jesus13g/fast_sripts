import tkinter as tk
from tkinter import ttk

def start_progress():
    progressbar.start(8)  # Inicia la animación de la barra de progreso (10ms de intervalo)
    progressbar['maximum'] = 1000  # Valor máximo de la barra de progreso
    progressbar['value'] = 0  # Valor inicial de progreso

    # Simula un progreso incrementando gradualmente el valor
    root.after(100, increment_progress)

def increment_progress():
    current_value = progressbar['value']
    if current_value < progressbar['maximum']:
        progressbar['value'] = current_value + 10  # Incrementa el valor de progreso en 10
        root.after(100, increment_progress)  # Actualiza cada medio segundo
    else:
        progressbar.stop()  # Detiene la animación cuando se alcanza el valor máximo

root = tk.Tk()

progressbar = ttk.Progressbar(root, mode='determinate', length=200)
progressbar.pack()

start_button = tk.Button(root, text='Iniciar', command=start_progress)
start_button.pack()

root.mainloop()
