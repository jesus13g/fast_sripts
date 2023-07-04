import tkinter as tk
from tkinter import ttk
import os
from re import findall
from glob import glob
from psutil import disk_partitions


class MakeFoldersApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Make Folders")
        self.geometry("700x300")
        self.configure(padx=30, pady=30)

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
        
        estilo.configure("TCombobox", font=("Helvetica", 12), 
                         foreground=self.color_verde, 
                         background=self.color_negroPantalla, 
                         fieldbackground=self.color_negroPantalla)
        
        estilo.configure("TButton", font=("Helvetica", 12), 
                         foreground="#000000", 
                         background=self.color_verde , 
                         hoverbackground= self.color_verdeFuerte)

        # Establecer el color de fondo de la ventana
        self.configure(bg= self.color_negroPantalla)
        
        ##################################      PARTICION       ###################################################
        # Crear el texto de la particion sleccionada 
        self.texto_particion = ttk.Label(self, text="Partición ", anchor='w', compound='right')
        self.texto_particion.grid(row=0, column=0, pady=5, sticky="w")
        
        # Toma de las particiones del sistema
        particiones = disk_partitions()
        txt_particiones = [p.mountpoint for p in particiones]
        
        # Crear el combox de la particion que se desea seleccionar
        self.entrada_particion = ttk.Combobox(self, values=tuple(txt_particiones), width=5)
        self.entrada_particion.grid(row=0, column=1, pady=5, sticky="w")
        
        # En caso de una unica particion
        if len(txt_particiones) == 1:
            self.entrada_particion.insert(0,txt_particiones[0])
        
        ##################################      RUTA       ###################################################
        # Crear el texto de la ruta a seleccionar
        self.texto_label_ruta = ttk.Label(self, text="Ruta ", anchor="w", compound="right")
        self.texto_label_ruta.grid(row=1, column=0, pady=5, sticky="w")
    
        # Crear la entrada de texto de la ruta
        self.rutas =[]
        self.entrada_ruta = ttk.Combobox(self, width=80, values=self.rutas)
        self.entrada_ruta.grid(row=1, column=1, pady=5)
        
        # Vincular la tecla "Control-KeyRelease" a la función de autocompletar ruta
        self.entrada_ruta.bind("<Control-KeyRelease>", self.autocompletar_ruta)
        self.entrada_ruta.bind("<Return>", self.obtener_texto)


        ##################################      NOMBRE CARPETA       ###################################################
        # Crear el texto de la carpeta a seleccionar
        self.texto_label_carpeta = ttk.Label(self, text="Nombre carpeta ", anchor="w")
        self.texto_label_carpeta.grid(row=2, column=0, pady=5, sticky="w")

        # Crear la entrada de texto del nombre de la carpeta
        self.entrada_carpeta = ttk.Entry(self, width=83)
        self.entrada_carpeta.grid(row=2, column=1, pady=5)


        ##################################      BOTON       ###################################################
        # Crear el botón
        self.boton = ttk.Button(self, text="Crear", command=self.obtener_texto)
        self.boton.grid(row=3, column=0, columnspan=2, pady=5)

        self.entrada_carpeta.bind("<Return>", self.obtener_texto)
        
        
        
        ##################################      RESULTADO       ###################################################
        # Crear el texto de salida resultado 
        self.texto_label = ttk.Label(self, text=" ")
        self.texto_label.grid(row=4, column=0, columnspan=2, pady=20)



    ##################################      METODOS       ###################################################
    def obtener_texto(self, event=None):
        ruta = self.entrada_particion.get() + self.entrada_ruta.get()

        if '/' in ruta:
            ruta.replace('/', '\\')

        carpeta = self.entrada_carpeta.get()
        print(carpeta)
        if ruta == '':
            self.texto_label.configure(text=f"Selecciona primero una ruta", foreground=self.color_rojoError)
        elif not self.validar_ruta(ruta):
            self.texto_label.configure(text=f"Ruta inválida", foreground=self.color_rojoError)
        elif carpeta == '':
            self.texto_label.configure(text=f"Da un nombre a la carpeta", foreground=self.color_rojoError)
        elif not self.validar_nombreCarpeta(carpeta):
            self.texto_label.configure(text=f"Nombre inválido", foreground=self.color_rojoError)
        else:
            self.crear_carpeta(ruta, carpeta)


    def validar_nombreCarpeta(self, carpeta: str):
        patron = r'[<>:"/\\|?*]'
        coincidencias = findall(patron, carpeta)
        return len(coincidencias) == 0


    def validar_ruta(self, ruta: str):
        if os.path.exists(ruta):
            return True
        else:
            return False


    def crear_carpeta(self, ruta, carpeta):
        ruta_carpeta = os.path.join(ruta, carpeta)

        if not os.path.exists(ruta_carpeta):
            os.mkdir(ruta_carpeta)
            self.texto_label.configure(text=f"Se ha creado la carpeta: {carpeta}", foreground=self.color_verde)
            self.entrada_carpeta.delete(0, tk.END)
        else:
            self.texto_label.configure(text=f"Ya existe la carpeta: {carpeta}", foreground=self.color_rojoError)
            self.entrada_carpeta.delete(0, tk.END)


    def autocompletar_ruta(self, event):
        ruta_ingresada = self.entrada_particion.get() + self.entrada_ruta.get()
        rutasCompleta = glob(ruta_ingresada + "*")
        posibles_rutas =  [ruta[3:] + '\\'  for ruta in rutasCompleta if os.path.isdir(ruta)]

        if len(posibles_rutas) == 1:
            ruta_completada = posibles_rutas[0] 
            self.entrada_ruta.delete(0, tk.END)
            self.entrada_ruta.insert(0, ruta_completada)
        if len(posibles_rutas) > 1:
            self.entrada_ruta['values'] = tuple(posibles_rutas)
            self.entrada_ruta.event_generate('<Down>')
            

    def run(self):
        self.mainloop()


# Crear la instancia de la aplicación y ejecutarla
app = MakeFoldersApp()
app.run()
