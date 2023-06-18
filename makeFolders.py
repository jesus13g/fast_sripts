import os
import sys
from tqdm import tqdm
import time

"""
Nos permite crear carpetas en un directorio deseado
"""

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
print(' Se van a crear las carpetas:')
print(" -"+ ' -'.join(list_namesFoldes) ) 

barra_progreso = tqdm(total=len(list_namesFoldes), 
                      bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}", 
                      ncols= 50)

for name in list_namesFoldes:
    barra_progreso.update()
    cpy_ruta = ruta + '\\' + name
    
    if not os.path.exists(cpy_ruta):
        os.makedirs(cpy_ruta)
    else:
        print('Existe la carpeta '+str(name))
    time.sleep(0.1)
        
barra_progreso.close()

