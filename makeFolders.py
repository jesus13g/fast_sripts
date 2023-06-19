import os
import sys
from tqdm import tqdm

"""
Nos permite crear carpetas en un directorio deseado
"""


def mostrar_resultados(yaExiste, creados):
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




if len(sys.argv) < 3:
    print('Parametros erroneos')
    exit(1)

# Ruta donde se crearan las carpetas
ruta = sys.argv[1] 

# Nombres de las carpetas a crear
namesFoldes = sys.argv[2]          

if not os.path.exists(ruta):    # Comprobamos si existe la ruta
    print('¡Error en la ruta seleccionada, NO existe!')


# Dividimos los nombres en una lsita
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

mostrar_resultados(yaExiste=yaExiste,creados=creados)
    

