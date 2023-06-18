from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
import sys


def weather_horas(driver:webdriver.Chrome):
    pass

def weather(ciudad, margen_tiempo):
    chrome_service = Service(r'C:\\Users\\balle\\Desktop\\chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()
    
    # Iniciamos la web que queremos hacer sraping
    driver.get('https://www.eltiempo.es/')
    
    # Se hace una espera de 5 seg para que se cargue la pagina
    WebDriverWait(driver, timeout=5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, # Seleccionamos un boton mediante su nombre de clase
                                'button.didomi-components-button.didomi-button.didomi-dismiss-button.didomi-components-button--color.didomi-button-highlight.highlight-button'))
        ).click()# ACEPTAMOS COOKIES

    WebDriverWait(driver, timeout=5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                'input#term'))
        ).send_keys(ciudad) # ESCRIBE BURGOS EN EL BUSCADOR

    WebDriverWait(driver, timeout=5).until(
        EC.element_to_be_clickable((By.XPATH, 
                                '/html/body/div[5]/header/div[3]/section/div[2]/div/div[1]/div/ul/li[1]/a'))
        ).click() #Seleccionamos la opcion de burgos 
    
    if margen_tiempo == "dias":
        WebDriverWait(driver, timeout=5).until(
        EC.element_to_be_clickable((By.XPATH, 
                                '/html/body/div[5]/div[1]/div[4]/div/main/section[3]/section/section/ul[1]/li[1]/h2/a'))
        ).click() # por dias
        
    elif margen_tiempo == "horas":
        WebDriverWait(driver, timeout=5).until(
        EC.element_to_be_clickable((By.XPATH, 
                                '/html/body/div[5]/div[1]/div[4]/div/main/section[3]/section/section/ul[1]/li[2]/h2/a'))
        ).click() # por horas        
        
        # /html/body/div[5]/div[1]/div[4]/div/main/section[3]/article/ul
        tabla_horas = driver.find_element(By.CLASS_NAME, 'days')
        filas = tabla_horas.find_elements(By.XPATH, './li')
        
        for fila in filas:
            datos_p = fila.find_elements(By.XPATH, './div/p')
            if len(datos_p) >= 2:
                hora = datos_p[0].text
                temperatura = datos_p[1].text
                print(f"Hora: {hora}, Temperatura: {temperatura}")
        
        
        
    time.sleep(8)



busqueda_ciudad = None
margen_tiempo = None
print(sys.argv)

if len(sys.argv) == 2:
    busqueda_ciudad = sys.argv[1]
    margen_tiempo = "dias"
elif len(sys.argv) == 3:
    busqueda_ciudad = sys.argv[2]
    if sys.argv[1] == '-d':
        margen_tiempo = "dias"
    elif sys.argv[1] == '-h':
        margen_tiempo = "horas"
    
    
weather(str(busqueda_ciudad), margen_tiempo=margen_tiempo)



