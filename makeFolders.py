import os,sys
from tqdm import tqdm

"""
Nos permite crear carpetas en un directorio deseado
"""


################################################################

def comprobar_variables(argumentos):
    if len(argumentos) < 3:
        print('Parametros erroneos')
        exit(1)

    # Ruta donde se crearan las carpetas
    ruta = argumentos[1] 

    if not os.path.exists(ruta):    # Comprobamos si existe la ruta
        print('¡Error en la ruta seleccionada, NO existe!')
        exit(1)

    if argumentos[2] == '-t':
        modo = True
    elif not argumentos[2].__contains__(','):   # Comprobamos una posible cadena correcta
        print('¡Error! los nombres las carpetas deben separarse con comillas')
        exit(1)
    # Nombres de las carpetas a crear
    namesFoldes = argumentos[2]          
    
    return ruta,namesFoldes,modo


####################################################################

def generar_folders(ruta, namesFolder,modo_teclado=False):
   if modo_teclado == True:
       generar_conTeclado(ruta) 
   else:
       generar_conArgumentos(ruta,namesFolder)
    # Dividimos los nombres en una lista
    

####################################################################

def generar_conTeclado(ruta):
    print('introduce un nombre para la carpeta')
    while True:
        name = input()
        if name == 'ok' or name == 'OK':
            break
        else:
            ruta_folder = ruta + '\\' + name
            if ' ' in name:
                print('Error, porfavor sin espacios')
                
            if os.path.exists(ruta):
                print('Error, esta carpeta ya existe')
                
            
        print('se creo ' + str(name))
    
    


####################################################################
def generar_conArguemnto(ruta,nameFolder):
    dict_namesFoldes = generarNombres(names=namesFolder)
    print(dict_namesFoldes)
    
    # Mostramos a lista
    n_name = len(list_namesFoldes)
    print('|' + '-----------------' * n_name + '|')
    print('| Se van a crear las carpetas:')
    print('| ' + ', '.join(list_namesFoldes).ljust(50) + '|')
    print('|' + '-----------------' * n_name + '|')
    
   

    # Lista con los nombres de los ficheros que ya existen 
    yaExiste = []
    # Lista con los nombres de los ficheros creados 
    creados = []

    for name in list_namesFoldes:
        barra_progreso.update()
        ruta_folder = ruta + '\\' + name
        
        if not os.path.exists(ruta_folder):
            os.makedirs(ruta_folder)
            creados.append(name)
        else:
            yaExiste.append(name)
        
    
    
    return yaExiste,creados

def generarNombres(names):
    pass



################################################################

def mostrar_resultados(yaExiste, creados):
    n_name = len(yaExiste) + len(creados)
    print('|' + '-----------------' * n_name + '|')
    print('| Se crearon las carpetas:')
    if creados != []:
        print('| ' + ', '.join(creados).ljust(50) + '|')
    else:
        print('| Ninguna'.ljust(50) + '|')

    print('|' + '-----------------' * n_name + '|')

    print('| Ya existian las carpetas:                       |')
    if yaExiste != []:
        print('| ' + ', '.join(yaExiste).ljust(50) + '|')
    else:
        print('| Ninguna'.ljust(50) + '|')


################################################################

##### MAIN #####
ruta,namesFolder,modo = comprobar_variables(sys.argv)

generar_folders(ruta=ruta,namesFolder=namesFolder,modo_teclado=modo)




