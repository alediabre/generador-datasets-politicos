import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import lxml
import string
import re
from utils.colores_consola import bcolors


# ==========================================

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


def scraping(usuario,num_max,fecha_ini,fecha_fin,mi_username,mi_password):
    '''
    Mediante un bot automatizado de Selenium, navega por Twitter.
    1)Introduce las credenciales del usuario que realiza el scraping
    2)Navega a la url que filtra por búsqueda avanzada según usuario y fechas
    Devuelve una lista de los tweets filtrados, concretamente de sus html con toda la informacion. El tweet en bruto
    '''

    #CREAR NAVEGADOR-------------------------------------------------------------------------------------
    
    bot = get_bot()

    #LOGIN-----------------------------------------------------------------------------------------------

    bot.get('https://twitter.com/i/flow/login')

    time.sleep(1)

    username_space = bot.find_element(By.XPATH,'//input[@autocomplete="username"]')
    username_space.send_keys(mi_username)
    username_space.send_keys(Keys.RETURN)

    time.sleep(1)

    try: 
        password_space = bot.find_element(By.XPATH,'//input[@name="password"]')
    except NoSuchElementException: #Si no existe el usuario
        bot.quit()
        print(f"{bcolors.FAIL}Error. El usuario introducido no existe{bcolors.ENDC}")
        return []

    password_space.send_keys(mi_password)
    password_space.send_keys(Keys.RETURN)

    time.sleep(2)

    #EXTRACCION----------------------------------------------------------------------------------------------

    if bot.current_url == "https://twitter.com/home": #Si el login ha tenido éxito
        print(f"{bcolors.OKGREEN}Login exitoso. Scrapping en proceso ...{bcolors.ENDC}")
    
        url = 'https://twitter.com/search?f=top&q=(from%3A'+str(usuario)+')%20until%3A'+str(fecha_fin)+'%20since%3A'+str(fecha_ini)+'&src=typed_query'
        bot.get(url)
        time.sleep(2)
        timeline = recuperar_tweets(bot,num_max)
        bot.quit()
        return timeline      
    else:
         bot.quit()
         print(f"{bcolors.FAIL}Error en las credenciales introducidas{bcolors.ENDC}")
         return []



def recuperar_tweets(bot,num):
    '''
    Recibe un navegador y el numero de tweets a recuperar, devuelve una lista con los html de los num primeros tweets recuperados
    Realiza un scroll para la búsqueda hasta llegar al número necesario o no encontrar más tweets
    '''
    tweets_almacenados = []
    tweets = []
    contador = 0

    while len(tweets) < num:
        contador += 1
        tweets_cargados = bot.find_elements(By.XPATH,'//article')
        if tweets_cargados == []:
            print(f"{bcolors.FAIL}Ha ocurrido un error en el scrapping. Revise su conexión y compruebe que existan tweets del usuario y fechas introducidos{bcolors.ENDC}")
            return []
        
        #Verificar y agregar tweets únicos a la lista
        for tweet in tweets_cargados:
            if tweet not in tweets_almacenados:
                tweets_almacenados.append(tweet)
                tweets.append(tweet.get_attribute("innerHTML"))
                contador = 0

        if contador > 3: #Si se realizan varios scrolls y no carga ningún tweet nuevo
            break

        bot.execute_script("window.scrollBy(0,600)", "")
        time.sleep(0.7)
        
    return tweets[:num]
    


def extraer_datos_tweets(usuario,lista_tweets):
    '''
    Recibe una lista de tweets (html) y devuelve las características autor, texto y hashtag de cada uno de ellos
    '''
    for article in lista_tweets:
        #Crear un objeto bs4 con el HTML obtenido
        soup = BeautifulSoup(article, "lxml")
        div_texto = soup.find("div", dir="auto")
        if div_texto != None:
            try:
                idioma = div_texto["lang"]
                if idioma != 'es': #Solo aceptamos español
                    continue
            except KeyError: #Si no tiene idioma significa que el tweet retweeteado ha sido eliminado
                continue

            #Dentro del div de texto, el texto se divide en distintos spans
            spans = div_texto.find_all("span")
            if len(spans) > 0:
                #Si el span contiene texto, se transforman sus caracteres espaciadores especiales en " "
                texto = [s.text.translate({ord(c): " " for c in string.whitespace}).strip() for s in spans if s.text != None]
                texto = " ".join(texto)

                hashtags = re.findall("#\w+", texto) #Almacenar posibles hasthags
                texto = re.sub("#\w+", "", texto) #Eliminar los hashtags del texto

            elem_autor = soup.find("a")
            autor = elem_autor["href"][1:]
            if autor != usuario:
                continue

        if (texto!="" and autor!=""):
            yield autor,texto,hashtags
