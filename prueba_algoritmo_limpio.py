
import pandas as pd
import time as t
import os
import cloudscraper


from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


import pytesseract as tess
tess.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from bs4 import BeautifulSoup

from funciones import lista_eventos_function,agrupacion_de_estadisticas,obtencion_estadisticas,funcion_shotmap,generador_archivos_excel,configuracion_driver,obtener_ligas_sofascore,obtener_ligas_pais

##Edge driver configuration

config_driver=configuracion_driver()
driver=config_driver[0]
headers=config_driver[1]
response=config_driver[2]
equipos=config_driver[3]

dic_ligas = obtener_ligas_sofascore(driver)
print('elegir Pais')
elegir_liga=input()
print(elegir_liga)
liga=dic_ligas[f"{elegir_liga}"]
print(liga)

liga_española = {}

## OBTENER LINKS DE LOS EVENTOS

# en caso de que la pagina tenga cloudfare y no quiera tomar la pagina
from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', })
url = driver.current_url
req = scraper.get(url)
print(req)
soup = BeautifulSoup(req.text, 'html.parser')
driver.get(liga)
ligas=obtener_ligas_pais(driver)
print('aqui elijes el la liga del pais seleccionado')
h = input()

liga_seleccionada = ligas[f"{h}"]
driver.get(liga_seleccionada)

while True:

    print('aqui elijes el equipo')
    comando = input('Ingrese a un equipo y de clic o ingrese c para CANCELAR')
    if comando == "c":
        break
    else:




        ## AQUI VA LA FUNCION lista_eventos()

        lista_eventos=lista_eventos_function(driver)


        nombre_equipo_elegido = driver.find_element(By.XPATH,
                                                    '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div[2]/h2').text

        liga_española[f'{nombre_equipo_elegido}'] = {}

        print(nombre_equipo_elegido)



        ####AQUI VA LA FUNCION SHOTMAP
        ruta_completa = f'LIGA_ESPAÑOLA/DATA_DISPAROS_POR_PARTIDO/{nombre_equipo_elegido}/'

        funcion_shotmap(ruta_completa,lista_eventos,headers,nombre_equipo_elegido)

        ##AQUI VA LA FUNCION OBTENER ESTADISTICAS
        contador = 0
        indice = 1
        while True:
            comando_control = ''

            lista_eventos = []
            state=True
            while state:
                try:
                    Estadisticas_obtenidas=obtencion_estadisticas(driver,indice,scraper,headers,liga_española,nombre_equipo_elegido)
                    statistics = Estadisticas_obtenidas[0]
                    liga_española = Estadisticas_obtenidas[1]
                    minute_values = Estadisticas_obtenidas[2]
                    nombre_partido = Estadisticas_obtenidas[3]
                    fecha = Estadisticas_obtenidas[4]
                    while True:

                        print('entré al bucle donde tomo cada partido')
                        lista_equipos = []
                        # comando_datos=input('clic magico')

                        # if comando_datos=='otro partido':
                        #  print('puedes elegir otro partido')
                        #  break
                        # else:
                        Estadisticas_obtenidas = obtencion_estadisticas(driver, indice, scraper, headers, liga_española,
                                                                        nombre_equipo_elegido)
                        statistics = Estadisticas_obtenidas[0]
                        print(f'aqui esta el estado de las estadisticas estadisticas:{statistics}')

                        if str(statistics) == '<Response [404]>':

                            print('hay error 404')
                            comando_404 = input(
                                '¿Quieres pasar a una siguiente pagina? en caso de que si presiona y en caso de que no ingresa "ter" en caso de que solo sea uno y falten ingresa "otro":')
                            if comando_404 == 'y':
                                try:
                                    driver.find_element(By.XPATH,
                                                        '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()
                                    indice = 1
                                    contador = 0
                                    print('cambiando de pagina y empezando de 0')
                                    t.sleep(3)

                                    break
                                except:
                                    input('esperemos que acomodes todo')
                            elif comando_404 == 'ter':
                                funcion_shotmap(ruta_completa)
                                # indice=1
                                break
                            elif comando_404 == 'otro':
                                contador += 1
                                indice += 1
                                # driver.find_element(By.XPATH,f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice+1}]').click()

                                break



                        else:
                            try:
                                estadisticas_grouped = agrupacion_de_estadisticas(statistics, contador, driver,
                                                                                  lista_equipos, nombre_equipo_elegido,
                                                                                  liga_española, indice, nombre_partido,
                                                                                  fecha, minute_values)
                                indice = estadisticas_grouped[2]

                                contador = estadisticas_grouped[1]

                                liga_española = estadisticas_grouped[0]
                                print(
                                    'ahora entré donde ocurre toda la magia donde se toman cada dato y se organiza en un json')
                                break
                            # Definir el script de JavaScript que mostrará el mensaje
                            except:
                                print('esperemos que acomodes')
                    break
                except:
                    state = False
                    c=input('esperemos que acomodes todo')
                    if c:
                        state=True
                        break

            print(contador)
            if contador == 10:
                print('ya tomaste todos los ejemplos, ahora que quieres hacer? cambiar pagina ingresa "ca" o terminar ingresa "terminamos"?')
                comando = input()
                if comando == 'ca':
                    try:
                        driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/button').click()
                        indice = 1
                        contador = 0
                        t.sleep(3)
                        funcion_shotmap(ruta_completa,lista_eventos,headers,nombre_equipo_elegido)
                    except:
                        input('esperemos que acomodes todo')

                elif comando == 'terminamos':
                    comando_control = comando
                    funcion_shotmap(ruta_completa,lista_eventos,headers,nombre_equipo_elegido)
                    break

            print('Siguiente partido')
            print(f'indice: {indice}')
            if comando_control == 'terminamos':
                funcion_shotmap(ruta_completa,lista_eventos,headers,nombre_equipo_elegido)

                break

dic_aux = {}

for key in liga_española.keys():
    for key2 in liga_española[key].keys():
        for key3 in liga_española[key][key2].keys():
            if key not in dic_aux:
                dic_aux[key] = {}
            dic_aux[key][key3] = liga_española[key][key2][key3]

# generando el excel

ruta=r'C:\Users\luis\Desktop\PORTFOLIO\projects\webscraping\webscraping\DATA_SOCCER\LIGA_ESPAÑOLA\extraCTOR\extraCTOR\LIGA_ESPAÑOLA\liga.xlsx'
generador_archivos_excel(ruta,dic_aux)
