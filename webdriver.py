import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.colores_consola import bcolors

# ==========================================

def wait_element(bot,time,css_selector,fail_message):
    '''
    Espera un tiempo "time" a que cargue un elemento por el bot.
    El elemento se busca por un selector css dado.
    En caso de no encontrarlo en el tiempo, imprime un mensaje de error y cierra el bot
    '''
    try:
        elemento = WebDriverWait(bot, time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return elemento
    except:
        print(f"{bcolors.BOLD}{bcolors.FAIL}{fail_message}{bcolors.ENDC}")
        bot.quit()


def get_bot(headless = False):
    '''
    Crea un navegador con unas opciones específicas. Si activamos el modo headless, no aparece en pantalla el navegador
    '''
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument("--headless")
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return bot


def scraping(orador,legislatura,paginacion):
    '''
    Mediante un bot automatizado de Selenium, navega por la web del cogreso.
    1)Introduce el filtro de la legislatura
    2)Introduce el filtro del orador
    3)Navega por las paginaciones hasta llegar a la dada por el parámetro paginacion. Va guardando los links que encuentra
    Devuelve un diccionario con los links para descargar los pdf, junto con una lista de las páginas que contienen las intervenciones
    '''

    ruta = 'https://www.congreso.es/es/busqueda-de-intervenciones'
    dict_pdf = dict()
    print(f"{bcolors.BOLD}\nRecuperando rutas de '{ruta}'...{bcolors.ENDC}")

    def guardar_links():
        '''
        Obtener los links del pdf de cada pleno. Guardarlos en dict_pdf = {clave: link , valor: paginas con intervenciones}

        '''
        selecciones_diputado = bot.find_elements(By.CSS_SELECTOR, 'tr[id^="sel_dip"]')

        for seleccion in selecciones_diputado:
            elem = seleccion.find_elements(By.CSS_SELECTOR, 'a')[4]
            
            enlace = elem.get_attribute('href')
            if 'public_oficiales' in enlace: #Previene errores si el enlace no es correcto
                link_pdf = enlace.split('#')
                pdf = link_pdf[0]
                pag = int(link_pdf[1].split('=')[1])

                if pdf not in dict_pdf.keys():
                    dict_pdf[pdf] = [pag]
                else:
                    paginas = dict_pdf[pdf]
                    paginas.append(pag)
                    dict_pdf[pdf] = sorted(paginas) #Listas ordenadas de paginas para que funcione más adelante como pila

    #CREAR NAVEGADOR----------------------------------------------------------------------------------------
    
    bot = get_bot()

    #BUSQUEDA-----------------------------------------------------------------------------------------------

    bot.get(ruta)
    
    #Introducir filtro de legislatura-----------------------------------------------------------------------
    filtro_legislatura = wait_element(bot,10,'select.legislaturas','La página no ha cargado correctamente. Revisa tu conexióno a internet')
    filtro_legislatura.click()

    opcion_legislatura = filtro_legislatura.find_element(By.CSS_SELECTOR, 'option[value="'+str(legislatura)+'"]')
    opcion_legislatura.click()
    time.sleep(1)

    #Introducir filtro de orador----------------------------------------------------------------------------

    filtro_orador = bot.find_element(By.CSS_SELECTOR, 'input.field.orador')
    filtro_orador.send_keys(orador)

    buscar = bot.find_element(By.CSS_SELECTOR, 'button[onclick="resetSavedSearchIntervenciones(); crearListado(1, 0)"]')
    buscar.click()
    time.sleep(1)

    #Navegar por las paginaciones guardando los links-------------------------------------------------------

    for i in range(paginacion):
        guardar_links()
        boton_siguiente = bot.find_elements(By.CSS_SELECTOR, '#_intervenciones_paginationLinksIntervenciones li.page-item a')[-2]
        bot.execute_script("arguments[0].scrollIntoView();", boton_siguiente)
        bot.execute_script("arguments[0].click();", boton_siguiente)
        print(f"{bcolors.BOLD}Paginación: {i+1}/{paginacion}{bcolors.ENDC}", end="\r")
        time.sleep(1.5)

    print(f"{bcolors.BOLD}{bcolors.OKGREEN}{len(dict_pdf.keys())} enlaces recuperados.{bcolors.ENDC}{bcolors.ENDC}")
    return dict_pdf



def get_oradores(legislatura):
    '''
    Mediante un bot automatizado de Selenium, navega por la web del cogreso.
    1)Introduce el filtro de la legislatura
    2)Despliega la lista de oradores
    Devuelve una lista de oradores existentes en la legislatura dada
    '''
    print(f"{bcolors.BOLD}\nBuscando oradores. Espere unos segundos...\n{bcolors.ENDC}")
    lista_oradores = []
    ruta = 'https://www.congreso.es/es/busqueda-de-intervenciones'
    bot = get_bot()
    bot.get(ruta)

    #Introducir filtro de legislatura-----------------------------------------------------------------------
    filtro_legislatura = wait_element(bot,10,'select.legislaturas','La página no ha cargado correctamente. Revisa tu conexióno a internet')
    filtro_legislatura.click()

    opcion_legislatura = filtro_legislatura.find_element(By.CSS_SELECTOR, 'option[value="'+str(legislatura)+'"]')
    opcion_legislatura.click()
    time.sleep(1)

    #Desplegar lista de oradores----------------------------------------------------------------------------
    mostrar_oradores = bot.find_element(By.CSS_SELECTOR, '#plus_fautor')
    mostrar_oradores.click()
    time.sleep(2)

    oradores = bot.find_elements(By.CSS_SELECTOR, 'ul.modalOradoresDiputados li')
    for orador in oradores:
        lista_oradores.append(orador.get_attribute('innerText'))

    return lista_oradores