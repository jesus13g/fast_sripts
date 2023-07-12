import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image
import subprocess

# Funciones de los botones
def boton1_click(icon, item):
    subprocess.run(['python', 'app_makeFolders.py'])
    
def boton2_click(icon, item):
    subprocess.run(['python', 'fastMaps.py'])



# Crear el menú desplegable
menu = (
    item('Make Folders', lambda: boton1_click(icon, item)),
    item('Fast Maps', lambda: boton2_click(icon, item))
)

# Cargar el icono
icon_image = Image.open("./img/icon_launcher.ico")

# Crear el icono en la bandeja del sistema
icon = pystray.Icon("nombre_icono", icon_image, "Fast Script", menu)

# Mostrar el icono en la bandeja del sistema
icon.run()
