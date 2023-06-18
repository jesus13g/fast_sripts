import webbrowser, sys, pyperclip
"""
Realiza una busqueda en google maps.
"""

if len(sys.argv) > 1:
    # Toma la direcion por argumento
    address = ' '.join(sys.argv[1:])
else:
    # toma la direccion del portapapeles
    address = pyperclip.paste()

# Realiza la busqueda con la direccion
webbrowser.open('https://www.google.com/maps/place/' + address)