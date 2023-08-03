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
        self.iconbitmap('.//img//icon_makeFolders.ico') # Establecer icono

        self.color_negroPantalla = '#292929'
        self.color_verde = '#308446'
        self.color_verdeFuerte = '#266a38'
        self.color_rojoError = '#ff0000'
        
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
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
        self.configure(bg=self.color_negroPantalla)
        
        
        ##################################      BTN AYUDA       ###################################################
        # Tomamos la img para el btn de ayuda
        self.img_btn_ayuda = tk.PhotoImage(file="./img/btn_ayuda.png")
        
        # Crear el btn 
        self.boton_ayuda = tk.Button(image=self.img_btn_ayuda, command=self.ventana_ayuda)
        self.boton_ayuda.configure(width=21, height=21)
        self.boton_ayuda.grid(row=0, column=1, pady=5,sticky="e")
        
        
        ##################################      PARTICION       ###################################################
        # Crear el texto de la particion sleccionada 
        self.texto_particion = ttk.Label(self, text="Partición ", anchor='w', compound='right')
        self.texto_particion.grid(row=1, column=0, pady=5, sticky="w")
        
        # Toma de las particiones del sistema
        particiones = disk_partitions()
        txt_particiones = [p.mountpoint for p in particiones]
        
        # Crear el combox de la particion que se desea seleccionar
        self.entrada_particion = ttk.Combobox(self, values=tuple(txt_particiones), width=5)
        self.entrada_particion.grid(row=1, column=1, pady=5, sticky="w")
        
        # En caso de una unica particion
        if len(txt_particiones) == 1:
            self.entrada_particion.insert(0,txt_particiones[0])
        
        
        ##################################      RUTA       ###################################################
        # Crear el texto de la ruta a seleccionar
        self.texto_label_ruta = ttk.Label(self, text="Ruta ", anchor="w", compound="right")
        self.texto_label_ruta.grid(row=2, column=0, pady=5, sticky="w")
    
        # Crear la entrada de texto de la ruta
        self.rutas =[]
        self.entrada_ruta = ttk.Combobox(self, width=80, values=self.rutas)
        self.entrada_ruta.grid(row=2, column=1, pady=5)
        
        # Vincular la tecla "Control-KeyRelease" a la función de autocompletar ruta
        self.entrada_ruta.bind("<Control-KeyRelease>", self.autocompletar_ruta)
        self.entrada_ruta.bind("<Return>", self.obtener_texto)


        ##################################      NOMBRE CARPETA       ###################################################
        # Crear el texto de la carpeta a seleccionar
        self.texto_label_carpeta = ttk.Label(self, text="Carpeta ", anchor="w")
        self.texto_label_carpeta.grid(row=3, column=0, pady=5, sticky="w")

        # Crear la entrada de texto del nombre de la carpeta
        self.entrada_carpeta = ttk.Entry(self, width=83)
        self.entrada_carpeta.grid(row=3, column=1, pady=5)
        
        # Crear el texto de las subcarpetas deseadas 
        self.texto_label_subcarpetas = ttk.Label(self, text="SubCarpetas ", anchor="w")
        self.texto_label_subcarpetas.grid(row=4, column=0, pady=5, sticky="w")

        # Crear la entrada de las posibles subcarpetas
        self.entrada_subcarpeta = ttk.Entry(self, width=83)
        self.entrada_subcarpeta.grid(row=4, column=1, pady=5)
        
        ##################################      BOTON       ###################################################
        # Crear el botón
        self.boton = ttk.Button(self, text="Crear", command=self.obtener_texto)
        self.boton.grid(row=5, column=0, columnspan=2, pady=5)

        self.entrada_carpeta.bind("<Return>", self.obtener_texto)        
        
        
        ##################################      RESULTADO       ###################################################
        # Crear el texto de salida resultado 
        self.texto_label = ttk.Label(self, text=" ")
        self.texto_label.grid(row=6, column=0, columnspan=2, pady=20)



    ##################################      METODOS       ###################################################
    
    """
    Obtiene las entradas para crear las carpetas. Previamente comprobara que se cumplen ciertas condiciones que 
    evitan fallos de codigo y mostrara un mesaje de error en caso de que se de una entrada incorrecta.
    """
    def obtener_texto(self, event=None):
        ruta = self.entrada_particion.get() + self.entrada_ruta.get()
        carpeta = self.entrada_carpeta.get()
        subCarpetas = self.validar_subCarpetas(self.entrada_subcarpeta.get())
        
        if '/' in ruta:
            ruta.replace('/', '\\')

        
        if ruta == '':
            self.texto_label.configure(text=f"Selecciona primero una ruta", foreground=self.color_rojoError)
            
        elif not self.validar_ruta(ruta):
            self.texto_label.configure(text=f"Ruta inválida", foreground=self.color_rojoError)
            
        elif carpeta == '':
            self.texto_label.configure(text=f"Da un nombre a la carpeta", foreground=self.color_rojoError)
            
        elif not self.validar_nombreCarpeta(carpeta):
            self.texto_label.configure(text=f"Nombre inválido", foreground=self.color_rojoError)
            
        elif subCarpetas == -1:
            self.texto_label.configure(text=f"Nombre subcarpeta inválido", foreground=self.color_rojoError)
            
        else:
            self.crear_carpetas(ruta, carpeta, subCarpetas)


    """
    Valida que la cadena pasada por argumento sea un nombre de carpeta valido, es decir, 
    no contiene ningun caracter como [<>:"/\\|?*].
    """
    def validar_nombreCarpeta(self, carpeta:str):
        patron = r'[<>:"/\\|?*]'
        coincidencias = findall(patron, carpeta)
        return len(coincidencias) == 0


    """
    Comprueba y valida que la ruta exista, en caso de que si devuelve True, en caso contrario False.
    """
    def validar_ruta(self, ruta:str):
        if os.path.exists(ruta):
            return True
        else:
            return False


    """
    En caso de que exista una entrada de las subcarpetas, divide la cadena en una lista de los
    nombres de las subcarpetas y comprueba que los nombres sean validos.
    """
    def validar_subCarpetas(self, subCarpetas:str):
        
        if subCarpetas == ' ':
            return 0
        
        subCarpetas = subCarpetas.replace(",", " ")
        list_subCarpetas = subCarpetas.split()
        
        if all(self.validar_nombreCarpeta(nombre) for nombre in list_subCarpetas):
            return list_subCarpetas
        else:
            return -1
            
    
    
    """
    Crea las carpetas, en la ruta seleccionada. En caso de que este la entrada de las subcarpetas
    las crea dentro de la carpeta primente creada. 
    """
    def crear_carpetas(self, ruta, carpeta, subCarpetas):
        ruta_carpeta = os.path.join(ruta, carpeta)
        
        if not os.path.exists(ruta_carpeta):
            os.mkdir(ruta_carpeta)
            if not subCarpetas:
                self.texto_label.configure(text=f"Se ha creado la carpeta: {carpeta}", foreground=self.color_verde)
            else: 
                for subcarp in subCarpetas:
                    ruta_subCarp = ruta_carpeta + '//' + subcarp
                    os.mkdir(ruta_subCarp)
                self.texto_label.configure(text=f"Se ha creado la carpeta: {carpeta} y sus subcarpetas", foreground=self.color_verde)
            self.entrada_carpeta.delete(0, tk.END)
            self.entrada_subcarpeta.delete(0, tk.END)
        else:
            self.texto_label.configure(text=f"Ya existe la carpeta: {carpeta}", foreground=self.color_rojoError)
            self.entrada_carpeta.delete(0, tk.END)
            self.entrada_subcarpeta.delete(0, tk.END)


    
    """
    Autocompleta la entrada de la ruta al pulsar la tecla CTRL, si solo existe una sola posible 
    entrada para autocompletar la autocompletara, si existen varias posibles rutas para autocompletar, se
    abrira un combox con las posibles rutas.
    """
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
            
    """
    Ventana de ayuda. Contendra un texto de explicacion del uso de la herramienta y
    una captura de un ejemplo de uso.
    """
    def ventana_ayuda(self):
        ventana_ayuda = tk.Toplevel(self)
        ventana_ayuda.title("Ayuda")
        ventana_ayuda.geometry("750x600")
        ventana_ayuda.configure(bg=self.color_negroPantalla)
        self.iconbitmap('.//img//icon_makeFolders.ico')

        # Crear el texto de ayuda
        texto = """
        Esta aplicación permite gestionar nuestro sistema de ficheros, creando carpetas 
        y subcarpetas.
    
        Para ello, el menú mostrará las siguientes entradas:
    
        - Partición: Se deberá elegir la partición donde queramos trabajar.
        - Ruta: Se escribirá la ruta donde deseamos crear nuestras carpetas.
            Se facilitará el autocompletado de la ruta al presionar la tecla CTRL.
        - Carpeta: Se escribirá el nombre de la carpeta a crear.
            (Se deben cumplir los caracteres válidos)
        - Subcarpeta: Se escribirá el o los nombres de las subcarpetas a crear, 
            cada nombre quedará separado por una coma.
            
        A continuación se muestra una captura con un ejemplo de uso.
        En este ejemplo, se creará en la ruta de una asignatura de la universidad la 
        carpeta 'Teoría' y dentro de ella las carpetas 'Tema1', 'Tema2', 'Tema3' y 'Tema4'.
        """
        label_texto = tk.Label(ventana_ayuda, justify=tk.LEFT, font=("Helvetica", 12), background=self.color_negroPantalla)
        label_texto.pack(pady=20, padx=20)
        label_texto.configure(text=texto, foreground=self.color_verde, anchor="nw")
        

        # Cargar y mostrar la imagen
        imagen = tk.PhotoImage(file="./img/img_capAyuda_makeFolders.PNG")
        label_imagen = tk.Label(ventana_ayuda, image=imagen)
        label_imagen.pack()
    
        ventana_ayuda.mainloop()

    """
    Metodo de activacion de la interfaz
    """
    def run(self):
        self.mainloop()


# Crear la instancia de la aplicación y ejecutarla
app = MakeFoldersApp()
app.run()
