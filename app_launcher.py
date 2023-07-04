import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image
import subprocess

# Funciones de los botones
def boton1_click(icon, item):
    subprocess.run(['python', 'app_makeFolders.py'])



# Crear el menú desplegable
menu = (
    item('Make Folders', lambda: boton1_click(icon, item)),
)

# Cargar el icono
icon_image = Image.open("icon_clip.jpeg")

# Crear el icono en la bandeja del sistema
icon = pystray.Icon("nombre_icono", icon_image, "Mi Aplicación", menu)

# Mostrar el icono en la bandeja del sistema
icon.run()
