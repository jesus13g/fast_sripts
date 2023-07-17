import webbrowser, sys, pyperclip
import tkinter as tk
from tkinter import ttk


"""
Realiza una busqueda en google maps.
"""

class fastMaps(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fast Maps")
        self.geometry("360x140")
        self.configure(padx=20, pady=20)
        self.wm_iconbitmap("./img/icon_fastMaps.ico") # Establecer icono

        self.color_negroPantalla = '#292929'
        self.color_verde = '#308446'
        self.color_verdeFuerte = '008000'
        self.color_rojoError = '#ff0000'
        
        estilo = ttk.Style(self)
        
        estilo.configure("TLabel", 
                         font=("Helvetica", 12), 
                         foreground=self.color_verde, 
                         background= self.color_negroPantalla)
        
        estilo.configure("TEntry",  
                         foreground= self.color_verde, # Color de fuente
                         background= self.color_negroPantalla, # Color de fondo
                         fieldbackground= self.color_negroPantalla)
        
        
        # Establecer el color de fondo de la ventana
        self.configure(bg=self.color_negroPantalla)
        
        ######################################      BTN AYUDA       ####################################################################
        # Tomamos la img para el btn de ayuda
        self.img_btn_ayuda = tk.PhotoImage(file="./img/btn_ayuda.png")
        
        # Crear el btn 
        self.boton_ayuda = tk.Button(image=self.img_btn_ayuda, command=self.ventana_ayuda)
        self.boton_ayuda.configure(width=21, height=21)
        self.boton_ayuda.grid(row=0, column=1, pady=3,sticky="e")
        
        ######################################      ORIGEN      ####################################################################
        self.text_origen = ttk.Label(self, text="Origen ", anchor='w', compound='right')
        self.text_origen.grid(row=1, column=0, pady=5, sticky="w")
        
        self.entrada_origen = ttk.Entry(self, width=40)
        self.entrada_origen.grid(row=1, column=1, pady=5, sticky="w")
        
        ######################################      DESTINO       ####################################################################
        self.text_destino = ttk.Label(self, text="Destino ", anchor='w', compound='right')
        self.text_destino.grid(row=2, column=0, pady=5, sticky="w")
        
        self.entrada_destino = ttk.Entry(self, width=40)
        self.entrada_destino.grid(row=2, column=1, pady=5, sticky="w")
        
        ######################################      ACTIVACIONES       ####################################################################
        self.entrada_origen.bind('<Return>', self.busqueda_googleMaps)
        self.entrada_destino.bind('<Return>', self.busqueda_googleMaps)
        
    
    """
    Realiza la busqueda en google maps 
    """
    def busqueda_googleMaps(self, event):
        origen = self.entrada_origen.get()
        destino = self.entrada_destino.get()
        
        if origen == '' and destino == '':
            pass    
        elif origen == '' and destino != '':
            webbrowser.open('https://www.google.com/maps/place/' + destino)
        elif origen != '' and destino == '':
            webbrowser.open('https://www.google.com/maps/place/' + origen)
        elif origen != '' and destino != '':
            webbrowser.open('https://www.google.com/maps/dir/'+origen+'/'+destino+'/')
        
    """
    Crea la ventana de ayuda 
    """
    def ventana_ayuda(self):
        top_level_window = tk.Toplevel(self)
        top_level_window.title("Ayuda")
        top_level_window.geometry("575x225")
        top_level_window.configure(bg=self.color_negroPantalla)

        # Crear el texto de ayuda
        texto = """
        Esta herramineta abre tu navegador y realiza una busqueda 
        en google Maps.
        
        Puedes realizar una busqueda de un único lugar, para ello escribe 
        el lugar en una de las dos entradas, sea la de origen o destino y 
        deja la otra vacia.
        
        Si deseas realizar una busqueda desde un lugar de origen a un 
        destino escribe los lugares en  sus respectivas entradas.
        """
        label_texto = tk.Label(top_level_window, justify=tk.LEFT, font=("Helvetica", 12), background=self.color_negroPantalla)
        label_texto.pack(pady=10, padx=20)
        label_texto.configure(text=texto)
        label_texto.configure(foreground=self.color_verde)
        label_texto.configure(anchor="nw")
    
        top_level_window.mainloop()
            
    
    def run(self):
        self.mainloop()
        
        


app = fastMaps()
app.run()