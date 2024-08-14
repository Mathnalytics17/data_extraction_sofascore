from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import pytesseract as tess

tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from bs4 import BeautifulSoup
import pandas as pd

from selenium.webdriver.common.by import By
import cloudscraper
import requests

import pytesseract as tess
tess.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import time as t

import os


def configuracion_driver():
    ##Edge driver configuration
    edge_driver_path = os.path.join(os.getcwd(), 'msedgedriver.exe')

    # Opciones de Edge
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    edge_service = Service(edge_driver_path)
    edge_options = Options()
    edge_options.add_argument(f'user-agent={user_agent}')

    # Inicializar el WebDriver con las opciones
    driver = webdriver.Edge(service=edge_service, options=edge_options)

    driver.get("https://www.sofascore.com/es/")
    t.sleep(2)
    # en caso de que la pagina tenga cloudfare y no quiera tomar la pagina

    scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', })
    url = 'https://www.sofascore.com/es/torneo/futbol/spain/laliga/8#id:52376'
    req = scraper.get(url)
    print(req)
    soup = BeautifulSoup(req.text, 'html.parser')
    # EQUIPOS DE LA LIGA
    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'if-none-match': 'W/"3525f8dd1c"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'If-Modified-Since': 'Mon, 22 Apr 2024 00:00:00 GMT'
    }

    response = scraper.get(
        'https://api.sofascore.com/api/v1/unique-tournament/8/season/52376/statistics/info',
        headers=headers,
        allow_redirects=True  # Ensure redirects are allowed
    )



    equipos = []
    for i in range(0, len(response.json()['teams'])):
        equipos.append(response.json()['teams'][i]['name'])


    headers = {
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'if-none-match': 'W/"5d04daf479"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'If-Modified-Since': 'Mon, 22 Apr 2024 00:00:00 GMT'
    }
    return driver,headers,response,equipos,scraper



def obtener_ligas_sofascore(driver):
    import re
    from selenium.webdriver.common.by import By

    # Localiza el div usando el XPath proporcionado
    div_element = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/div/div[1]/div[5]/div/div[2]')

    # Encuentra todos los elementos <a> dentro de este div
    links = div_element.find_elements(By.TAG_NAME, 'a')

    # Crear un diccionario para almacenar los enlaces
    links_dict = {}

    # Expresión regular para eliminar números y saltos de línea
    cleaning_pattern = re.compile(r'[\n\d]+')

    # Extrae los href de cada enlace y utiliza el texto del enlace como clave
    for link in links:
        link_text = link.text.strip()  # Texto visible en el enlace
        link_text = cleaning_pattern.sub('', link_text)  # Limpia el texto
        link_text = link_text.strip()  # Elimina espacios adicionales después de limpiar

        link_href = link.get_attribute('href')  # El atributo href del enlace
        if link_text:  # Solo agrega si hay texto en el enlace
            links_dict[link_text] = link_href

    # Imprime el diccionario de enlaces limpio
    print("Diccionario de enlaces:")
    for key, value in links_dict.items():
        print(f"{key}: {value}")
    return links_dict


def obtener_ligas_pais(driver):
    import re
    from selenium.webdriver.common.by import By

    # Localiza el div usando el XPath proporcionado
    div_element = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[2]/div/div[4]/div')

    # Encuentra todos los elementos <a> dentro de este div
    links = div_element.find_elements(By.TAG_NAME, 'a')

    # Crear un diccionario para almacenar los enlaces
    links_dict = {}

    # Expresión regular para eliminar números y saltos de línea
    cleaning_pattern = re.compile(r'[\n\d]+')

    # Extrae los href de cada enlace y utiliza el texto del enlace como clave
    for link in links:
        link_text = link.text.strip()  # Texto visible en el enlace
        link_text = cleaning_pattern.sub('', link_text)  # Limpia el texto
        link_text = link_text.strip()  # Elimina espacios adicionales después de limpiar

        link_href = link.get_attribute('href')  # El atributo href del enlace
        if link_text:  # Solo agrega si hay texto en el enlace
            links_dict[link_text] = link_href
        # Imprime el diccionario de enlaces limpio
        print("Diccionario de enlaces:")
    for key, value in links_dict.items():
        print(f"{key}: {value}")

    return links_dict

def lista_eventos_function(driver):
    lista_eventos = []
    for i in range(0, 11):
        try:
            id_evento = driver.find_element(By.XPATH,
                                            f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{i}]/a')

            equipos_evento = driver.find_element(By.XPATH,
                                                 f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{i}]/a').text

            url1 = id_evento.get_attribute("href")
            # print(url1)
            # Dividir la URL por el caracter ":" y extraer el último elemento
            id_part = url1.split(':')[-1]
            # Imprimir el ID
            # Dividir la cadena en partes usando '\n' como separador
            partes = equipos_evento.split('\n')

            # Seleccionar los elementos que necesitas (en este caso, los terceros y cuartos elementos)
            equipos = [partes[2], partes[3], partes[2] + ' ' + 'vs' + ' ' + partes[3]]

            lista_eventos.append((id_part, equipos))

        except:
            pass

    print(lista_eventos)
    return lista_eventos


def funcion_shotmap(ruta_completa,lista_eventos,headers,nombre_equipo_elegido):
    # Columnas del DataFrame
    columnas_shot = ['Nombre', 'isHome', 'shotType', 'situation', 'bodyPart', 'goalMouthLocation',
                     'goalMouthCoordinates_x', 'goalMouthCoordinates_y', 'goalMouthCoordinates_z',
                     'time', 'draw_start', 'draw_block', 'draw_end', 'draw_goal', 'incidentType']
    shotmap_por_partido = {}

    # Crear la carpeta
    if not os.path.exists(ruta_completa):
        os.makedirs(ruta_completa)
    # Iterar sobre cada evento en lista_eventos
    for evento in lista_eventos:

        id_evento = evento[0]

        shotmap = requests.get(f'https://api.sofascore.com/api/v1/event/{id_evento}/shotmap', headers=headers)
        nombre_equipo_select = evento[1][0]
        nombre_partido = evento[1][2]
        datos_disparos = []

        # Intenta obtener los disparos del evento
        try:
            disparos_evento = shotmap.json()['shotmap']
        except KeyError:
            disparos_evento = []  # Si no hay disparos disponibles, crea una lista vacía

        # Iterar sobre cada disparo en los disparos del evento
        for disparo in disparos_evento:
            # Intenta acceder a las claves en el diccionario, maneja errores si la clave no existe
            try:
                jugador = disparo['player']['name']
            except KeyError:
                jugador = None

            try:
                isHome = disparo['isHome']
            except KeyError:
                isHome = None

            try:
                shotType = disparo['shotType']
            except KeyError:
                shotType = None

            try:
                situation = disparo['situation']
            except KeyError:
                situation = None

            try:
                bodyPart = disparo['bodyPart']
            except KeyError:
                bodyPart = None

            try:
                goalMouthLocation = disparo['goalMouthLocation']
            except KeyError:
                goalMouthLocation = None

            try:
                goalMouthCoordinates = disparo['goalMouthCoordinates']
                goalMouthCoordinates_x = goalMouthCoordinates['x']
                goalMouthCoordinates_y = goalMouthCoordinates['y']
                goalMouthCoordinates_z = goalMouthCoordinates['z']
            except KeyError:
                goalMouthCoordinates_x = None
                goalMouthCoordinates_y = None
                goalMouthCoordinates_z = None

            try:
                time = disparo['time']
            except KeyError:
                time = None

            try:
                draw_start = disparo['draw']['start']
            except KeyError:
                draw_start = None

            try:
                draw_block = disparo['draw']['block']
            except KeyError:
                draw_block = None

            try:
                draw_end = disparo['draw']['end']
            except KeyError:
                draw_end = None

            try:
                draw_goal = disparo['draw']['goal']
            except KeyError:
                draw_goal = None

            try:
                incidentType = disparo['incidentType']
            except KeyError:
                incidentType = None

            # Agregar los datos del disparo a la lista de eventos
            datos_disparos.append([jugador, isHome, shotType, situation, bodyPart, goalMouthLocation,
                                   goalMouthCoordinates_x, goalMouthCoordinates_y, goalMouthCoordinates_z,
                                   time, draw_start, draw_block, draw_end, draw_goal, incidentType])

        # Agregar los datos del evento al diccionario de eventos por partido para el equipo
        if nombre_equipo_select not in shotmap_por_partido:
            shotmap_por_partido[nombre_equipo_select] = {}

        shotmap_por_partido[nombre_equipo_select][nombre_partido] = datos_disparos

        # Crear la carpeta para el equipo si no existe
        ruta_equipo = f'LIGA_ESPAÑOLA/DATA_DISPAROS_POR_PARTIDO/{nombre_equipo_elegido}/{nombre_equipo_select}/'
        if not os.path.exists(ruta_equipo):
            os.makedirs(ruta_equipo)

        # Crear un archivo de Excel para el partido con los datos de disparos
        with pd.ExcelWriter(f'{ruta_equipo}{nombre_partido}.xlsx') as writer:
            # Convertir los datos del partido en un DataFrame
            df_partido = pd.DataFrame(datos_disparos, columns=columnas_shot)
            if len(nombre_partido) > 31:
                # Elimina los espacios y divide la cadena en palabras
                palabras = nombre_partido.split()
                # Elimina las primeras palabras hasta que la longitud de la cadena sea menor o igual a 31
                while len(' '.join(palabras)) > 31:
                    palabras.pop(0)
                # Reconstruye la cadena con las palabras restantes
                nombre_partido = ' '.join(palabras)

            # Escribir el DataFrame en la hoja correspondiente
            df_partido.to_excel(writer, sheet_name=nombre_partido, index=False)

        # Imprimir confirmación
        print(f"Archivos de Excel creados exitosamente para {nombre_equipo_select} - {nombre_partido}.")


def obtencion_estadisticas(driver,indice,scraper,headers,liga_española,nombre_equipo_elegido):
    global nombre_partido
    comando_control = ''

    lista_eventos = []
    for i in range(0, 11):
        try:
            id_evento = driver.find_element(By.XPATH,
                                            f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{i}]/a')

            equipos_evento = driver.find_element(By.XPATH,
                                                 f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{i}]/a').text

            url1 = id_evento.get_attribute("href")
            # print(url1)
            # Dividir la URL por el caracter ":" y extraer el último elemento
            id_part = url1.split(':')[-1]
            # Imprimir el ID
            # Dividir la cadena en partes usando '\n' como separador
            partes = equipos_evento.split('\n')

            # Seleccionar los elementos que necesitas (en este caso, los terceros y cuartos elementos)
            equipos = [partes[2], partes[3], partes[2] + ' ' + 'vs' + ' ' + partes[3]]

            lista_eventos.append((id_part, equipos))

        except:
            pass

    print('aqui se extren las estadisticas', f'indice {indice}')
    t.sleep(2)
    driver.find_element(By.XPATH,
                        f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice}]').click()
    fecha = driver.find_element(By.XPATH,
                                f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice}]/a/div/div/div[2]').text
    # t.sleep(2)

    try:
        nombre_partido = driver.find_element(By.XPATH,
                                             '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]').text + ' ' + 'vs' + ' ' + driver.find_element(
            By.XPATH,
            '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[3]').text
        fecha = driver.find_element(By.XPATH,
                                    f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice}]/a/div/div/div[2]').text
        t.sleep(2)
    except:
        driver.find_element(By.XPATH,
                            f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice}]').click()
        fecha = driver.find_element(By.XPATH,
                                    f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice}]/a/div/div/div[2]').text
        t.sleep(2)

    # nombre_partido=driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]').text + ' '+ 'vs' + ' ' + driver.find_element(By.XPATH,'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[3]').text
    liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'] = {}
    # print(id_evento_actual)
    try:
        for i in range(0, len(lista_eventos)):
            if nombre_partido in lista_eventos[i][1][2]:
                id_evento_actual = lista_eventos[i][0]
        statistics = scraper.get(f'https://api.sofascore.com/api/v1/event/{id_evento_actual}/statistics',
                                 headers=headers, allow_redirects=True)
    except:
        statistics = 'None'

    try:
        attack_momentum = scraper.get(f'https://api.sofascore.com/api/v1/event/{id_evento_actual}/graph',
                                      headers=headers, allow_redirects=True)
        # Datos del attack momentum en crudo

        data = attack_momentum.json()['graphPoints']
        data
        # Crear un diccionario con los datos
        minute_values = {item['minute']: item['value'] if item['value'] < 0 else 0 for item in data}

        minute_values
    except:
        minute_values = {}
    print(nombre_partido)
    return statistics,liga_española,minute_values,nombre_partido,fecha


def agrupacion_de_estadisticas(statistics,contador,driver,lista_equipos,nombre_equipo_elegido,liga_española,indice,nombre_partido,fecha,minute_values):
    print('ahora entré donde ocurre toda la magia donde se toman cada dato y se organiza en un json')
    contador += 1
    local = driver.find_element(By.XPATH,
                                '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[1]').text
    visitante = driver.find_element(By.XPATH,
                                    '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[3]').text
    competicion = driver.find_element(By.XPATH,
                                      '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[1]/ul/li[2]/a').text
    gol_local_partido = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]').text.split()[
        0]
    gol_visitante_partido = driver.find_element(By.XPATH,
                                                '//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]').text.split()[
        2]
    lista_equipos.append(local)
    lista_equipos.append(visitante)
    print(lista_equipos[0])
    resultado_w_l_d = driver.find_element(By.XPATH,
                                          f'//*[@id="__next"]/main/div[2]/div/div[2]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div[{indice}]').text[
        -1]
    if lista_equipos[0] == nombre_equipo_elegido or lista_equipos[0] in nombre_equipo_elegido or \
            lista_equipos[0] == 'Atl. Madrid' or lista_equipos[0] == 'Celta' or lista_equipos[
        0] == 'Girona' or lista_equipos[0] == 'Alavés':
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}'] = {}
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}']['local'] = 'Si'
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}']['competicion'] = competicion
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}'][f'Resultado'] = resultado_w_l_d
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}'][f'goles_equipo'] = gol_local_partido
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}'][f'goles_rival'] = gol_visitante_partido
        for j in range(0, len(statistics.json()['statistics'][0]['groups'])):
            if len(statistics.json()['statistics'][0]['groups'][j]['statisticsItems']) > 1:
                for i in range(0,
                               len(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'])):
                    nombre_estadistica = \
                        statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['name']
                    valor_estadistica = \
                        statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['away']
                    # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['name'])
                    # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['away'])
                    liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
                        f'{lista_equipos[1]}_local_{competicion}_{fecha}'][
                        f'{nombre_estadistica}'] = valor_estadistica
            else:
                # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['name'])
                # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['away'])
                nombre_estadistica = \
                    statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['name']
                valor_estadistica = \
                    statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['away']
                liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
                    f'{lista_equipos[1]}_local_{competicion}_{fecha}'][
                    f'{nombre_estadistica}'] = valor_estadistica
        print('datos tomados cuando es local')
        indice += 1
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[1]}_local_{competicion}_{fecha}'].update(minute_values)
        # print(liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}'][f'{lista_equipos[1]}'])
    else:
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}'] = {}
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}']['local'] = 'No'
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}']['competicion'] = competicion
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}'][f'Resultado'] = resultado_w_l_d
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}'][f'goles_equipo'] = gol_visitante_partido
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}'][f'goles_rival'] = gol_local_partido

        for j in range(0, len(statistics.json()['statistics'][0]['groups'])):
            if len(statistics.json()['statistics'][0]['groups'][j]['statisticsItems']) > 1:
                # print(liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}'][f'{lista_equipos[0]}'])
                for i in range(0,
                               len(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'])):
                    nombre_estadistica = \
                        statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['name']
                    valor_estadistica = \
                        statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['home']
                    # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['name'])
                    # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][i]['away'])
                    liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
                        f'{lista_equipos[0]}_away_{competicion}_{fecha}'][
                        f'{nombre_estadistica}'] = valor_estadistica


            else:
                # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['name'])
                # print(statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['away'])
                nombre_estadistica = \
                    statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['name']
                valor_estadistica = \
                    statistics.json()['statistics'][0]['groups'][j]['statisticsItems'][0]['home']
                liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
                    f'{lista_equipos[0]}_away_{competicion}_{fecha}'][
                    f'{nombre_estadistica}'] = valor_estadistica
        liga_española[f'{nombre_equipo_elegido}'][f'{nombre_partido}_{fecha}'][
            f'{lista_equipos[0]}_away_{competicion}_{fecha}'].update(minute_values)
        print('datos tomados cuando es visitante')
        indice += 1
    return liga_española,contador,indice

def generador_archivos_excel(ruta,dic_aux):
    with pd.ExcelWriter(ruta) as writer:
        # Itera sobre cada equipo y escribe sus rivales en una hoja separada
        for equipo, rivales in dic_aux.items():
            # Convierte los datos del equipo en un DataFrame
            df_equipo = pd.DataFrame(rivales).T
            # Verifica si la longitud de la cadena es mayor que 31
            if len(equipo) > 31:
                # Elimina los espacios y divide la cadena en palabras
                palabras = equipo.split()
                # Elimina las primeras palabras hasta que la longitud de la cadena sea menor o igual a 31
                while len(' '.join(palabras)) > 31:
                    palabras.pop(0)
                # Reconstruye la cadena con las palabras restantes
                nueva_cadena = ' '.join(palabras)
                print(nueva_cadena)

            # Escribe el DataFrame en la hoja correspondiente
            df_equipo.to_excel(writer, sheet_name=equipo)