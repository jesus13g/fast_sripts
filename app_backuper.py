import shutil,os,datetime,zipfile
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from psutil import disk_partitions
from glob import glob



class app_backuper(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Backuper")
        self.geometry("700x300")
        self.configure(padx=30, pady=30)
        self.iconbitmap('.//img//icon_backuper.ico') # Establecer icono

        self.color_negroPantalla = '#292929'
        self.color_verde = '#308446'
        self.color_verdeFuerte = '#008000'
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
        self.configure(bg=self.color_negroPantalla)
        
    
    ########################----------      Disposicion de los frames       ----------#########################################
        # Creamos un canvas que servira como borde 
        self.canvas_borde = tk.Canvas(self, bg=self.color_verde)#bg=self.color_verde
        
        # Creamos los frames 
        self.frame_btnIniciales = tk.Frame(self, background=self.color_negroPantalla) #  , background=self.color_negroPantalla
        self.frame_text_foldersBackup = tk.Frame(self.canvas_borde, background=self.color_negroPantalla)
        self.frame_rutaDest = tk.Frame(self)
        self.frame_btnBackup = tk.Frame(self, background=self.color_negroPantalla)
        
        # Empaquetamos los frames y los canvas ajustandos
        self.frame_btnIniciales.pack(padx=10, pady=2, anchor="nw", fill="x", expand=True)
        self.canvas_borde.pack(pady=2, anchor="nw", fill="x", expand=True)
        self.frame_text_foldersBackup.pack(padx=8, pady=8, anchor="nw", fill="x", expand=True)
        self.frame_rutaDest.pack(padx=8, pady=8, anchor="nw", fill="x", expand=True)
        self.frame_btnBackup.pack(padx=10, pady=2, anchor="nw")
        
        # Enlazamos el evento que ajusta el canvas con el frame 
        self.canvas_borde.bind("<Configure>", lambda event: self.dibujar_borde)
        
   
    ##################################      BTN AYUDA [frame_btnIniciales]      ###################################################
        # Tomamos la img para el btn de ayuda
        self.img_btn_ayuda = tk.PhotoImage(file="./img/btn_ayuda.png")
        
        # Crear el btn 
        self.boton_ayuda = tk.Button(self.frame_btnIniciales, image=self.img_btn_ayuda, command=self.ventana_ayuda)
        self.boton_ayuda.configure(width=21, height=21)
        self.boton_ayuda.pack(side="left", padx=40, pady=2)
        
        
    ##################################      BTN select folder backup [frame_btnIniciales]       ###################################################
        self.boton_selectBackup = tk.Button(self.frame_btnIniciales, text="Selección de carpeta", command=self.abrir_explorador)
        self.boton_selectBackup.pack(side="left", padx=10, pady=2)
        
        self.boton_clearLast = tk.Button(self.frame_btnIniciales, text="Clear Last", command=self.clearLast)
        self.boton_clearLast.pack(side="left", padx=10, pady=2)
        
        self.boton_clearAll = tk.Button(self.frame_btnIniciales, text="Clear All", command=self.clearAll)
        self.boton_clearAll.pack(side="left", padx=10, pady=2)
        
        
    ##################################      LIST folders backup [frame_text_foldersBackup]       ###################################################
        #Lista y cadena para las distintas rutas de los directorios que se haran backup
        self.list_foldersToBackup = []
        self.cadena_foldersToBackup = ""
        self.text_foldersToBackup = ttk.Label(self.frame_text_foldersBackup, text=self.cadena_foldersToBackup)
        self.text_foldersToBackup.pack(anchor="nw", padx=10, pady=2)
        
        
    ##################################      ENTRADA ruta destino  [frame_rutaDest]       ###################################################
        
        self.texto_rutaDest = ttk.Label(self.frame_rutaDest, text="Ruta destino del backup")
        self.texto_rutaDest.grid(row=0, column=0, padx=10, pady=5) 
        
        particiones = disk_partitions()
        txt_particiones = [p.mountpoint for p in particiones]
        
        # Crear el combox de la particion que se desea seleccionar
        self.entrada_particion = ttk.Combobox(self.frame_rutaDest, values=tuple(txt_particiones), width=5)
        self.entrada_particion.grid(row=0, column=1, padx=10, pady=5)
        
        # En caso de una unica particion
        if len(txt_particiones) == 1:
            self.entrada_particion.insert(0,txt_particiones[0])
        
        self.rutas_dest =[]
        self.entrada_ruta_dest = ttk.Combobox(self.frame_rutaDest, width=50, values=self.rutas_dest)
        self.entrada_ruta_dest.grid(row=0, column=2, padx=10, pady=5) 
        
        self.entrada_ruta_dest.bind("<Control-KeyRelease>", self.autocompletar_ruta)
        
    ##################################      BTN inicio del backup [frame_btnBackup]       ###################################################
        self.boton_inicioBackup = tk.Button(self.frame_btnBackup, text="Iniciar backup", command=self.backup(self.list_foldersToBackup, self.entrada_ruta_dest.get(), "nombre"))
        self.boton_inicioBackup.pack(anchor="w", padx=10, pady=2)
    
  
  ##################################      METODOS      ###################################################
              
        
    def abrir_explorador(self):
        carpeta_seleccionada = filedialog.askdirectory()
        
        if carpeta_seleccionada == "":
            pass
        elif carpeta_seleccionada not in self.list_foldersToBackup:   
            self.add_rutaBackup(carpeta_seleccionada)
        else:
            self.mostrar_ventana_error_directorioDuplicado(carpeta_seleccionada)
     
     
    def add_rutaBackup(self, nueva_carpeta):
        self.list_foldersToBackup.append(nueva_carpeta)
        self.cadena_foldersToBackup += "- " + nueva_carpeta + "\n"
        self.text_foldersToBackup.config(text=self.cadena_foldersToBackup)
    
    
    def clearLast(self):
        if len(self.list_foldersToBackup) != 0:
            self.list_foldersToBackup.pop()
            text = self.cadena_foldersToBackup.splitlines()
            
            if text:
                text = text[:-1]
                
            self.cadena_foldersToBackup = '\n'.join(text) + '\n'
            self.text_foldersToBackup.config(text=self.cadena_foldersToBackup)
        
        
    def clearAll(self):
        self.list_foldersToBackup.clear()
        self.cadena_foldersToBackup = ""
        self.text_foldersToBackup.config(text=self.cadena_foldersToBackup)
        
    
    def autocompletar_ruta(self, event):
        ruta_ingresada = self.entrada_particion.get() + self.entrada_ruta_dest.get()
        rutasCompleta = glob(ruta_ingresada + "*")
        posibles_rutas =  [ruta[3:] + '\\'  for ruta in rutasCompleta if os.path.isdir(ruta)]

        if len(posibles_rutas) == 1:
            ruta_completada = posibles_rutas[0] 
            self.entrada_ruta_dest.delete(0, tk.END)
            self.entrada_ruta_dest.insert(0, ruta_completada)
        if len(posibles_rutas) > 1:
            self.entrada_ruta_dest['values'] = tuple(posibles_rutas)
            self.entrada_ruta_dest.event_generate('<Down>')
    
    
    def backup(self, rutas_orig, ruta_dest, nombre_backup):
        print("inicio backup")
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archivo_respaldo = os.path.join(ruta_dest, f"{nombre_backup}-{fecha_actual}.zip")

        with zipfile.ZipFile(archivo_respaldo, 'w') as zipf:
            for ruta_orig in rutas_orig:
                for carpeta_actual, _, archivos in os.walk(ruta_orig):
                    for archivo in archivos:
                        ruta_completa = os.path.join(carpeta_actual, archivo)
                        ruta_relativa = os.path.relpath(ruta_completa, ruta_orig)
                        zipf.write(ruta_completa, ruta_relativa)
        print("fin backup")
               

    def mostrar_ventana_error_directorioDuplicado(self, direct_duplicado):
        ventana_error = tk.Toplevel()
        ventana_error.title("Error")
        
        mensaje = 'Ha ocurrido un error. Ya se selecciono el directorio: \n' + direct_duplicado
        
        etiqueta_mensaje = tk.Label(ventana_error, text=mensaje)
        etiqueta_mensaje.pack(padx=20, pady=20)
        
        boton_cerrar = tk.Button(ventana_error, text="Cerrar", command=ventana_error.destroy)
        boton_cerrar.pack(pady=10)       
    
    
    """
    Ajusta y dibuja en canvas para crear la sensacion de borde
    """
    def dibujar_borde(self):
        x1, y1, x2, y2 = self.canvas_borde.bbox("all")  # Obtener las coordenadas del borde del canvas
        self.canvas_borde.create_rectangle(x1, y1, x2, y2, outline="green", width=2)  # Dibujar el rectángulo del borde
    
            
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
        Texto ayuda
        """
        label_texto = tk.Label(top_level_window, justify=tk.LEFT, font=("Helvetica", 12), background=self.color_negroPantalla)
        label_texto.pack(pady=10, padx=20)
        label_texto.configure(text=texto)
        label_texto.configure(foreground=self.color_verde)
        label_texto.configure(anchor="nw")
    
        top_level_window.mainloop()     
    
    
    def run(self):
        self.mainloop()
        
        
app = app_backuper()
app.run()
                    
