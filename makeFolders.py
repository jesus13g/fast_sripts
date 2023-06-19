import os
import sys
from tqdm import tqdm
import time
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

    if not argumentos[2].__contains__(','):   # Comprobamos una posible cadena correcta
        print('¡Error! los nombres las carpetas deben separarse con comillas')
        exit(1)
    # Nombres de las carpetas a crear
    namesFoldes = argumentos[2]          

    if not os.path.exists(ruta):    # Comprobamos si existe la ruta
        print('¡Error en la ruta seleccionada, NO existe!')
        exit(1)

    return ruta,namesFoldes


####################################################################

def generar_folders(ruta, namesFoldes):
    # Dividimos los nombres en una lista
    namesFoldes = namesFoldes.replace(",", " ")
    list_namesFoldes = namesFoldes.split()

    # Mostramos a lista
    n_name = len(list_namesFoldes)
    print('|' + '-----------------' * n_name + '|')
    print('| Se van a crear las carpetas:')
    for name in list_namesFoldes:
        print(f"| - {name} ".ljust(50) + '|')
    print('|' + '-----------------' * n_name + '|')

    barra_progreso = tqdm(total=n_name, 
                        bar_format="| {l_bar}{bar} {n_fmt}/{total_fmt} procesos ", 
                        ncols= 40)

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
        
    barra_progreso.close()
    
    return yaExiste,creados

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
inicio = time.time()
ruta,namesFoldes = comprobar_variables(sys.argv)

yaExiste,creados = generar_folders(ruta=ruta,namesFoldes=namesFoldes)

mostrar_resultados(yaExiste=yaExiste,creados=creados)

fin = time.time()
print(fin-inicio)

