import pystray
from pystray import MenuItem as item
from PIL import Image
import subprocess

def boton_makeFolders(icon, item):
    subprocess.run(['python', 'app_makeFolders.py'])

def boton_fastMaps(icon, item):
    subprocess.run(['python', 'app_fastMaps.py'])

menu = [
    item('Make Folders', lambda: boton_makeFolders(icon, item)),
    item('Fast Maps', lambda: boton_fastMaps(icon, item))
]

icon_image = Image.open("./img/icon_launcher.ico")
icon = pystray.Icon("nombre_icono", icon_image, "Fast Script", menu)
icon.run()
