import webbrowser, sys, pyperclip
"""
toma los argumentos o el portafolios de la busqueda de google maps
"""

if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address)