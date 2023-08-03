import shutil,os,datetime,zipfile,threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from psutil import disk_partitions
from glob import glob
from re import findall



class app_backuper(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.backup_manager = backup()
        
        self.title("Backuper") # Damos el nombre de la ventana 
        
        self.long_y = 350
        self.dimension_ventana = f"800x{str(self.long_y)}"
        self.geometry(self.dimension_ventana)
        self.resizable(False, False)
        
        self.configure(padx=30, pady=30)
        self.iconbitmap('.//img//icon_backuper.ico') # Establecer icono

        self.color_negroPantalla = '#292929'
        self.color_grisOscuro = '#212121'
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
        
        estilo.configure("TCombobox", font=("Helvetica", 12,), 
                         foreground=self.color_verde, 
                         background=self.color_negroPantalla, 
                         fieldbackground=self.color_negroPantalla)
        
        estilo.configure("TButton", font=("Helvetica", 10), 
                         foreground="#000000", 
                         background=self.color_verde , 
                         focusbackground = self.color_verdeFuerte)
    
        
        
        # Establecer el color de fondo de la ventana
        self.configure(bg=self.color_negroPantalla)
         
        
    ########################----------      Disposicion de los frames       ----------#########################################
        # Creamos un canvas que servira como borde 
        self.canvas_borde = tk.Canvas(self, bg=self.color_verde)#bg=self.color_verde
        
        # Creamos los frames 
        self.frame_btnIniciales = tk.Frame(self, background=self.color_negroPantalla) #  , background=self.color_negroPantalla
        self.frame_text_foldersBackup = tk.Frame(self.canvas_borde, background=self.color_negroPantalla)
        self.frame_rutaDest = tk.Frame(self, background=self.color_negroPantalla)
        self.frame_nombreBackup = tk.Frame(self, background=self.color_negroPantalla)
        self.frame_btnBackup = tk.Frame(self, background=self.color_negroPantalla)
        
        # Empaquetamos los frames y los canvas ajustandos
        self.frame_btnIniciales.pack(padx=10, pady=2, anchor="nw", fill="y", expand=True)
        self.canvas_borde.pack(pady=2, anchor="nw", fill="x", expand=True)
        self.frame_text_foldersBackup.pack(padx=8, pady=8, anchor="nw", fill="x", expand=True)
        self.frame_rutaDest.pack(padx=8, pady=8, anchor="nw", fill="y", expand=True)
        self.frame_nombreBackup.pack(padx=8, pady=8, anchor="nw", fill="y", expand=True)
        self.frame_btnBackup.pack(padx=10, pady=2, anchor="nw", fill="y")
        
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
        self.boton_selectBackup = ttk.Button(self.frame_btnIniciales, text="Selección de carpeta", command=self.abrir_explorador_orig)
        self.boton_selectBackup.pack(side="left", padx=10, pady=2)
        
        self.boton_clearLast = ttk.Button(self.frame_btnIniciales, text="Clear Last", command=self.clearLast)
        self.boton_clearLast.pack(side="left", padx=10, pady=2)
        
        self.boton_clearAll = ttk.Button(self.frame_btnIniciales, text="Clear All", command=self.clearAll)
        self.boton_clearAll.pack(side="left", padx=10, pady=2)
        
        self.boton_tipoRespaldo = ttk.Button(self.frame_btnIniciales, text=".zip", command=self.swap_tipoRespaldo)
        self.boton_tipoRespaldo.pack(side="left", padx=10, pady=2)
    
    
        
    ##################################      LIST folders backup [frame_text_foldersBackup]       ###################################################
        #Lista y cadena para las distintas rutas de los directorios que se haran backup
        self.list_foldersToBackup = []
        self.cadena_foldersToBackup = ""
        self.text_foldersToBackup = ttk.Label(self.frame_text_foldersBackup, text=self.cadena_foldersToBackup)
        self.text_foldersToBackup.pack(anchor="nw", padx=10, pady=2)
        
        
    ##################################      ENTRADA ruta destino  [frame_rutaDest]       ###################################################
        self.texto_rutaDest = tk.Button(self.frame_rutaDest, text="Ruta destino del backup", command=self.abrir_explorador_dest,
                                        font=("Helvetica", 12), 
                                        bg=self.color_negroPantalla,
                                        fg=self.color_verde,
                                        activebackground=self.color_grisOscuro,
                                        activeforeground=self.color_verde,
                                        highlightbackground=self.color_negroPantalla,)
        
        self.texto_rutaDest.grid(row=0, column=0, padx=10, pady=5) 
        
        particiones = disk_partitions()
        self.txt_particiones = [p.mountpoint for p in particiones]
        
        # Crear el combox de la particion que se desea seleccionar
        self.entrada_particion = ttk.Combobox(self.frame_rutaDest, values=tuple(self.txt_particiones), width=5)
        self.entrada_particion.grid(row=0, column=1, padx=10, pady=5)
        
        # En caso de una unica particion
        if len(self.txt_particiones) == 1:
            self.entrada_particion.insert(0,self.txt_particiones[0])
        
        self.rutas_dest =[]
        self.entrada_ruta_dest = ttk.Combobox(self.frame_rutaDest, width=50, values=self.rutas_dest)
        self.entrada_ruta_dest.grid(row=0, column=2, padx=10, pady=5) 
        
        self.entrada_ruta_dest.bind("<Control-KeyRelease>", self.autocompletar_ruta)
        
        
    ##################################      Nombre backup  [frame_nombreBackup]       ###################################################
        self.text_nombreBackup = ttk.Label(self.frame_nombreBackup, text="Nombre backup")
        self.text_nombreBackup.grid(row=0, column=0, padx=10, pady=5)
        
        self.entrada_nombreBackup = ttk.Entry(self.frame_nombreBackup, width=64)
        self.entrada_nombreBackup.grid(row=0, column=1, padx=75, pady=5)
        
        
    ##################################      BTN inicio del backup [frame_btnBackup]       ###################################################
        self.boton_inicioBackup = ttk.Button(self.frame_btnBackup, text="Iniciar backup", command=self.validar_backup)
        self.boton_inicioBackup.grid(row=0, column=0, padx=10, pady=2)
    
  
    ##################################      Salida del backup(o errores) [frame_btnBackup]       ###################################################
        self.salida = ""
        self.text_salida = ttk.Label(self.frame_btnBackup, text=self.salida)
        self.text_salida.grid(row=0, column=1, padx=86, pady=2)
    
    
    
  ##################################      METODOS DE INTERFAZ      ###################################################       
    """
    Abre el explorador de archivos y permite seleccionar unicamente carpetas, si no se ha tomado la añade a la lista
    en caso contrario muestra una ventana de error.
    """   
    def abrir_explorador_orig(self):
        carpeta_seleccionada = filedialog.askdirectory()
        
        if carpeta_seleccionada == "":
            pass
        elif carpeta_seleccionada not in self.list_foldersToBackup:   
            self.add_rutaBackup(carpeta_seleccionada)
            self.redimension_ventana()
            
        else:
            self.mostrar_ventana_error_directorioDuplicado(carpeta_seleccionada)
    
    
    
    def redimension_ventana(self):
        self.long_y += 10
        self.dimension_ventana = f"800x{str(self.long_y)}"
        self.geometry(self.dimension_ventana)
        
        
    """
    Selecciona la carpeta de destino 
    """
    def abrir_explorador_dest(self):
        carpeta_seleccionada = filedialog.askdirectory()
        carpeta_seleccionada = carpeta_seleccionada.replace("/","\\")
        print(carpeta_seleccionada)
        
        if carpeta_seleccionada == "":
            pass
        else:
            particion = carpeta_seleccionada[:3]
            ruta = carpeta_seleccionada[3:]
            self.put_rutaDest(particion=particion, ruta=ruta)
        
         
    """
    Escribe la ruta de destino a partir de la particion + ruta
    """     
    def put_rutaDest(self, particion, ruta):
        if particion in self.txt_particiones:
            self.entrada_particion.delete(0, 'end')
            self.entrada_particion.insert(0, self.txt_particiones[self.txt_particiones.index(particion)])
        
        self.entrada_ruta_dest.delete(0, 'end')   
        self.entrada_ruta_dest.insert(0, ruta)
           
       
    """
    Cambia el tipo del que sera el respaldo
    """    
    def swap_tipoRespaldo(self):
        if self.boton_tipoRespaldo.cget('text') == '.zip':
            self.boton_tipoRespaldo.config(text='.tar')
        elif self.boton_tipoRespaldo.cget('text') == '.tar':
            self.boton_tipoRespaldo.config(text='.zip')
     
     
    """
    Añade la ruta del dirctorio para el backup.
    """
    def add_rutaBackup(self, nueva_carpeta):
        self.list_foldersToBackup.append(nueva_carpeta)
        self.cadena_foldersToBackup += "- " + nueva_carpeta + "\n"
        self.text_foldersToBackup.config(text=self.cadena_foldersToBackup)
    
    
    """
    Elimina el ultimo directorio añadido de la lista de directorios para backup.
    """
    def clearLast(self):
        if len(self.list_foldersToBackup) != 0:
            self.list_foldersToBackup.pop()
            text = self.cadena_foldersToBackup.splitlines()
            
            if text:
                text = text[:-1]
                
            self.cadena_foldersToBackup = '\n'.join(text) + '\n'
            self.text_foldersToBackup.config(text=self.cadena_foldersToBackup)
        
        
    """
    limpia completamente la lista de directorios para backup.
    """   
    def clearAll(self):
        self.list_foldersToBackup.clear()
        self.cadena_foldersToBackup = ""
        self.text_foldersToBackup.config(text=self.cadena_foldersToBackup)
        
    
    """
    Autocompleta la entrada de la ruta al pulsar la tecla CTRL, si solo existe una sola posible 
    entrada para autocompletar la autocompletara, si existen varias posibles rutas para autocompletar, se
    abrira un combox con las posibles rutas.
    """
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
            self.entrada_ruta_dest.selection_clear()
            
    
    """
    Ajusta y dibuja en canvas para crear la sensacion de borde
    """
    def dibujar_borde(self):
        x1, y1, x2, y2 = self.canvas_borde.bbox("all")  # Obtener las coordenadas del borde del canvas
        self.canvas_borde.create_rectangle(x1, y1, x2, y2, outline="green", width=2)  # Dibujar el rectángulo del borde       
            
            
            
    ##################################      METODOS DE VALIDACION      ###################################################
    """
    Valida todos los datos necesarios para que se cree un backup correcto. Los datos a validar seran:
            - Las rutas de origen de las cuales se va hacer el backup (si existen)
            - La ruta de destino donde se va a guardar el backup (si existe)
            - El nombre de salida del backup (no contiene caracteres inadecuados)
    En caso de que se validen todos los datos se ejecutara el backup.
    """
    def validar_backup(self):
        if not self.validar_rutasOrig():
            self.error_validacion("Las rutas de origen son erroneas.")
            
        elif not self.validar_rutaDest():
            self.error_validacion("La ruta de destino para el respaldo es erronea.")
            
        elif not self.validar_nombreBackup():
            self.error_validacion("El nombre para el respaldo contiene caracteres inadecuados")
        
        else:
            backup_type = self.boton_tipoRespaldo.cget('text')
            thread = threading.Thread(target=self.create_backup, args=(backup_type,))
            thread.start()
    
    
    """
    Valida las rutas del backup
    """
    def validar_rutasOrig(self):
        for ruta in self.list_foldersToBackup:
            if not self.validar_rutaExistente(ruta=ruta):
                return False
        return True
    
    
    """
    Valida la ruta destino
    """
    def validar_rutaDest(self):
        return self.validar_rutaExistente(self.entrada_particion.get() + self.entrada_ruta_dest.get())
    
    
    """
    Valida el nombre del backup
    """
    def validar_nombreBackup(self):
        patron = r'[<>:"/\\|?*]'
        coincidencias = findall(patron, self.entrada_nombreBackup.get())
        return len(coincidencias) == 0
    
    
    """
    Valida que la ruta pasada por argumento exista en el ordenador donde se ejecute.
    """
    def validar_rutaExistente(self, ruta:str):
        if os.path.exists(ruta):
            return True
        else:
            return False
    
    
    
    ##################################      METODOS DE ERRORES/AYUDA      ###################################################
    """
    Muestra un error de validación, que se pasa por argumento.
    """
    def error_validacion(self, error:str):
        self.text_salida.configure(text=error, foreground=self.color_rojoError)
    
               
    """
    Crea y muestra una ventana con un mensaje de error de que sea intentado seleccionar un directorio que 
    ya se habia seleccionado con anterioridad.
    """
    def mostrar_ventana_error_directorioDuplicado(self, direct_duplicado):
        ventana_error = tk.Toplevel(self)
        ventana_error.title("Error")
        ventana_error.resizable(False, False)
        ventana_error.iconbitmap('.//img//icon_backuper.ico') # Establecer icono
        
        mensaje = 'Ha ocurrido un error. Ya se selecciono el directorio: \n' + direct_duplicado
        
        etiqueta_mensaje = tk.Label(ventana_error, text=mensaje)
        etiqueta_mensaje.pack(padx=20, pady=20)
        
        boton_cerrar = ttk.Button(ventana_error, text="Cerrar", command=ventana_error.destroy)
        boton_cerrar.pack(pady=10)       
     
            
    """
    Crea la ventana de ayuda 
    """
    def ventana_ayuda(self):
        ventana_ayuda = tk.Toplevel(self)
        ventana_ayuda.title("Ayuda")
        ventana_ayuda.geometry("675x775")
        ventana_ayuda.resizable(False, False)
        ventana_ayuda.configure(bg=self.color_negroPantalla)
        ventana_ayuda.iconbitmap('.//img//icon_backuper.ico') # Establecer icono        
        
        # Crear el texto de ayuda
        texto_inicial = """
        Con esta aplicacion se podra realizar un backup, una copia de seguridad 
        de nuestros archivos, permitiendo crear archivos de respaldo de distintos
        tipos, ".zip" o ".tar".
        
        Entre los botones de arriba encontramos varias acciones ,el primero de 
        todos, nos permitira seleccionar el directorio del que se hara el respaldo, 
        podremos seleccionar varias. A continuación tendremos dos botones uno 
        que eliminara la ultima carpeta seleccionada, Clear Last, y otro que 
        eliminara la lista completa de los directorios seleccionados, Clear All. 
        El último boton en esta linea permitira alternar entre los dos formatos 
        del respaldo.
        """
        
        texto_intermedio = """
        Ademas acontinuacion deberemos de seleccionar el directorio de destino 
        donde se guardara nuestro backup, podremos escribir la ruta de destino
        que se autocompletara al dar a la tecla CTRL si deseamos o podemos dar
        al boton a su izq que nos abrira una ventana de seleccion. Por último
        daremos un nombre a nuestro respaldo, el cual tendra la fecha de realización.
        """
        texto_final = """
        Por ultimo tendremos el boton que inicia el proceso de backup.
        
        El menu es intuitivo y facil de usar ademas de que en caso de
        faltar un dato o dar un error se mostrara un mensaje que le guie 
        en el utilizamiento de la aplicacion.
        """
        
        label_texto_inicial = tk.Label(ventana_ayuda, text=texto_inicial, 
                                       font=("Helvetica", 12), 
                                       background=self.color_negroPantalla, 
                                       anchor="nw", foreground=self.color_verde)
        label_texto_inicial.pack(pady=10, padx=10)
    
        imagen1 = tk.PhotoImage(file="./img/img_capAyuda_backup1.PNG")
        img_btnSuperiores = tk.Label(ventana_ayuda, image=imagen1)
        img_btnSuperiores.pack(anchor="n")
        
        label_texto_intermedio = tk.Label(ventana_ayuda, text=texto_intermedio, 
                                          font=("Helvetica", 12), 
                                          background=self.color_negroPantalla, 
                                          anchor="nw", foreground=self.color_verde)
        label_texto_intermedio.pack(pady=10, padx=10)
    
        imagen2 = tk.PhotoImage(file="./img/img_capAyuda_backup2.PNG")
        img_btnIntermedio = tk.Label(ventana_ayuda, image=imagen2)
        img_btnIntermedio.pack(anchor="n")
        
        label_texto_final = tk.Label(ventana_ayuda, text=texto_final, 
                                     font=("Helvetica", 12), 
                                     background=self.color_negroPantalla, 
                                     anchor="nw", foreground=self.color_verde)
        label_texto_final.pack(pady=10, padx=10)
    
        
        ventana_ayuda.mainloop()     
        
        
    def create_backup(self, backup_type):
        try:
            # Toma el tipo del backup
            rutas_orig = self.list_foldersToBackup
            ruta_dest = self.entrada_particion.get() + self.entrada_ruta_dest.get()
            nombre_backup = self.entrada_nombreBackup.get()

            self.text_salida.config(text="Proceso iniciado...", foreground=self.color_verde)

            if backup_type == '.zip':
                self.backup_manager.backup_zip(rutas_orig, ruta_dest, nombre_backup)
            elif backup_type == '.tar':
                self.backup_manager.backup_tar(rutas_orig, ruta_dest, nombre_backup)

            # Update the output text after backup completion
            self.text_salida.config(text="Backup completado correctamente!", foreground=self.color_verde)
            
        except Exception as e:
            msg_error = f"Un error ocurrio durante el backup: {str(e)}"
            self.text_salida.config(text=msg_error, foreground=self.color_rojoError)

    
    ######### RUN #########
    def run(self):
        self.mainloop()




class backup:
    def __init__(self):
        pass

    
    def backup_zip(self, rutas_orig, ruta_dest, nombre_backup):
        archivo_respaldo = os.path.join(ruta_dest, f"{nombre_backup}.zip")
        with zipfile.ZipFile(archivo_respaldo, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ruta_orig in rutas_orig:
                for carpeta_actual, _, archivos in os.walk(ruta_orig):
                    for archivo in archivos:
                        ruta_completa = os.path.join(carpeta_actual, archivo)
                        ruta_relativa = os.path.relpath(ruta_completa, ruta_orig)
                        zipf.write(ruta_completa, os.path.join(os.path.basename(ruta_orig), ruta_relativa))
        return archivo_respaldo


    def backup_tar(self, rutas_orig, ruta_dest, nombre_backup):
        archivo_respaldo = os.path.join(ruta_dest, f"{nombre_backup}.tar")
        with tarfile.open(archivo_respaldo, 'w') as tar:
            for ruta_orig in rutas_orig:
                for carpeta_actual, _, archivos in os.walk(ruta_orig):
                    for archivo in archivos:
                        ruta_completa = os.path.join(carpeta_actual, archivo)
                        ruta_relativa = os.path.relpath(ruta_completa, ruta_orig)
                        tar.add(ruta_completa, arcname=os.path.join(os.path.basename(ruta_orig), ruta_relativa))
        return archivo_respaldo

        
        
app = app_backuper()
app.run()
                    
