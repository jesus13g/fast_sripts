import tkinter as tk
from tkinter import ttk

def start_progress():
    progressbar.start(8)  # Inicia la animación de la barra de progreso (10ms de intervalo)

def stop_progress():
    progressbar.stop()  # Detiene la animación de la barra de progreso

root = tk.Tk()

progressbar = ttk.Progressbar(root, mode='indeterminate', length=200)
progressbar.pack()

start_button = tk.Button(root, text='Iniciar', command=start_progress)
start_button.pack()

stop_button = tk.Button(root, text='Detener', command=stop_progress)
stop_button.pack()

root.mainloop()
