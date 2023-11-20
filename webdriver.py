import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import shutil,os,requests,re
import pdfplumber
import pandas as pd

# ==========================================

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def scraping(orador,legislatura,paginacion):

    ruta = 'https://www.congreso.es/es/busqueda-de-intervenciones'
    dict_pdf = dict()
    print(f"{bcolors.BOLD}Recuperando rutas de '{ruta}'...{bcolors.ENDC}")

    def guardar_links():
    #Obtener los links de los pdf de los plenos. Guardarlos en dict_pdf, clave: link , valor: paginas con intervenciones
        selecciones_diputado = bot.find_elements(By.CSS_SELECTOR, 'tr[id^="sel_dip"]')

        for seleccion in selecciones_diputado:
            elem = seleccion.find_elements(By.CSS_SELECTOR, 'a')[4]
            link_pdf = elem.get_attribute('href').split('#')
            pdf = link_pdf[0]
            pag = int(link_pdf[1].split('=')[1])

            if pdf not in dict_pdf.keys():
                dict_pdf[pdf] = [pag]
            else:
                paginas = dict_pdf[pdf]
                paginas.append(pag)
                dict_pdf[pdf] = sorted(paginas) #Listas ordenadas de paginas para que haga de pila

    #CREAR NAVEGADOR-------------------------------------------------------------------------------------
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    #options.add_argument("--headless")
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    #BUSQUEDA-----------------------------------------------------------------------------------------------

    bot.get(ruta)
    time.sleep(1)

    #Introducir filtro de legislatura

    filtro_legislatura = bot.find_element(By.CSS_SELECTOR, 'select.legislaturas')
    filtro_legislatura.click()

    opcion_legislatura = filtro_legislatura.find_element(By.CSS_SELECTOR, 'option[value="'+str(legislatura)+'"]')
    opcion_legislatura.click()
    time.sleep(1)

    #Introducir filtro de orador

    filtro_orador = bot.find_element(By.CSS_SELECTOR, 'input.field.orador')
    filtro_orador.send_keys(orador)

    buscar = bot.find_element(By.CSS_SELECTOR, 'button[onclick="resetSavedSearchIntervenciones(); crearListado(1, 0)"]')
    buscar.click()
    time.sleep(1)

    #Navegar por las paginaciones guardando los links

    for i in range(paginacion):
        guardar_links()
        boton_siguiente = bot.find_elements(By.CSS_SELECTOR, '#_intervenciones_paginationLinksIntervenciones li.page-item a')[-2]
        bot.execute_script("arguments[0].scrollIntoView();", boton_siguiente)
        bot.execute_script("arguments[0].click();", boton_siguiente)
        print(f"{bcolors.BOLD}Paginación: {i+1}/{paginacion}{bcolors.ENDC}", end="\r")
        time.sleep(1)

    print(f"{bcolors.BOLD}{bcolors.OKGREEN}{len(dict_pdf.keys())} enlaces recuperados.{bcolors.ENDC}{bcolors.ENDC}")
    return dict_pdf



def descargar_documentos(pdf_dict,carpeta_destino):

    shutil.rmtree(carpeta_destino)
    os.makedirs('pdf')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Connection": "keep-alive",
    }

    for i,link in enumerate(pdf_dict.keys()):
        print(f"{bcolors.BOLD}Descargando documentos: {i}/{len(pdf_dict.keys())}{bcolors.ENDC}", end='\r')
        response = requests.get(link, headers=headers)
        if response.status_code == 200:

            nombre_archivo = link.split('oficiales/')[1].replace('/','_')
            ruta_archivo = f"{carpeta_destino}/{nombre_archivo}"
            with open(ruta_archivo, 'wb') as f:
                f.write(response.content)

        else: print(f"{bcolors.WARNING}No se ha podido recuperar el archivo {link} correctamente. Código: {response.status_code}{bcolors.ENDC}")
    
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}Documentos correctamente descargados en {carpeta_destino}\n{bcolors.ENDC}{bcolors.ENDC}")



def extraer_textos(orador, ruta, paginas):
    #Regla1: Comenzar tras el primer ":" después de orador en mayúscula (o en minúsculas entre paréntesis)
    #Regla2: Terminar en la línea anterior al siguiente nombre en negrita y mayúscula
    #Regla3: Eliminar contenido entre paréntesis y saltos de línea
    lista_fragmentos = []
    num_paginas = len(paginas)

    def comenzar_fragmento(texto,vista):
        #Para encontrar el inicio busca el nombre del orador en mayúsculas, o en minúsculas entre paréntesis
        #Si la pagina ha sido vista antes, se busca la siguiente aparición
        orador_en_parentesis = orador.title()
        matches_inicio = list(re.finditer(rf'{orador}.*:|[A-Z]\w+[A-Z]\s\({orador_en_parentesis}\):', texto))
        if len(matches_inicio)>vista:
            return texto[matches_inicio[vista].end():].strip()
        else: return False
        
    def esNegrita(palabra,cadena,caracteres):
        #Devuelve si una palabra está en negrita, para ello comprueba la propiedad 'fontname' del primer caracter
        match_palabra = re.search(palabra, cadena)
        first_char = caracteres[match_palabra.start()]
        if "Bold" in first_char["fontname"]:
            return True
        else: return False
            
    def terminar_fragmento(texto,cadena,caracteres):
        #Para encontrar el final va recorriendo las palabras mayusculas hasta encontrar una en negrita
        matches = re.finditer(r'(^|\n).*([A-Z]\w+[A-Z])',texto)
        for match_fin in matches:
            palabra = match_fin.group(2)
            if esNegrita(palabra,cadena,caracteres):
                return texto[:match_fin.start()]
        return False
    
    def crop_page(pagina,x0,top,x1,bottom):
        #Recorta la pagina de forma que solo incluya el texto relevante
        my_bbox = (x0,top,x1,bottom)
        page_crop = pagina.crop(bbox=my_bbox)
        return page_crop

    
    with pdfplumber.open(ruta) as pdf:

        pagina_anterior = False
        vista = 0
        p_origen = paginas[0] #Primera página en la pila de páginas, de la que se parte para extraer un fragmento
        p = p_origen #Variable para iterar sobre la primera página de la pila, hasta encontrar el final del fragmento

        def avanzar_pagina():
            #Se elimina la página más alta en la pila actualmente y se actualiza la variable con la nueva pagina mas alta
            #Incrementa el numero de vistas si la página es la misma que la ya vista (hay una doble intervención)
            nonlocal p_origen, p, vista
            if len(paginas) > 1:
                vista = vista+1 if paginas[0] == paginas[1] else 0
                paginas.remove(p_origen)
                p_origen = paginas[0]
                p = p_origen
            else: paginas.remove(p_origen)

        while len(paginas)>0:
            print(f'{bcolors.BOLD}Página: {num_paginas-len(paginas)}/{num_paginas}{bcolors.ENDC}', end='\r') #Imprime el progreso de paginas
            pagina = pdf.pages[p-1]
            pagina_recortada = crop_page(pagina,50.0,100.0,550.0,780.0)
            texto = pagina_recortada.extract_text()   #Texto normal de la pagina
            caracteres = pagina_recortada.chars   #Lista de caracteres de la pagina con sus propiedades
            cadena = "".join(c['text'] for c in caracteres) #Encadenamiento de los caracteres. Aqui las letras tienen los mismos indices que en caracteres

            #Si no hay pagina anterior, se busca la cota inicial. Si la hay, la cota es toda la pagina
            if pagina_anterior == False: 
                cota_fragmento = comenzar_fragmento(texto,vista)
            else:
                cota_fragmento = texto

            #Si en la pagina indicada en paginas, no se encuentra el nombre, no hay cota (suele ser por errata).Se avanza en la pila
            if cota_fragmento == False: 
                pagina_anterior = False
                avanzar_pagina()
            else:
                fragmento = terminar_fragmento(cota_fragmento,cadena,caracteres)
                #Si no se ha encontrado el final de la intervencion en la pagina, se pasa a la siguiente y se añade la cota actual a la pagina anterior
                if fragmento == False:
                    pagina_anterior = pagina_anterior+cota_fragmento if pagina_anterior != False else cota_fragmento
                    p+=1
                else: 
                    #Si hay parte del fragmento en la pagina anterior, se juntan, y se restablece a False la pagina anterior
                    if pagina_anterior != False:
                        fragmento = pagina_anterior+fragmento
                        pagina_anterior = False

                    #Limpiar fragmento -> Eliminar paréntesis y el punto si lo precede. Eliminar saltos de linea
                    fragmento_limpio = re.sub(r'\n',' ',re.sub(r'\.\s\([^\(]*\)|\([^\(]*\)', '', fragmento))
                    nombre_doc = ruta.split("/")[2].split(".")[0]
                    lista_fragmentos.append((orador,nombre_doc,fragmento_limpio))
                    avanzar_pagina()

    return lista_fragmentos


def recuperar_informacion(orador,legislatura,paginacion):

    lista_textos = []
    pdf_dict = scraping(orador,legislatura,paginacion)
    carpeta_destino = "./pdf"
    descargar_documentos(pdf_dict,carpeta_destino)

    nombre = orador.split(',')[0].upper()
    for archivo in pdf_dict:
        nombre_archivo = archivo.split('oficiales/')[1].replace('/','_')
        ruta = f"{carpeta_destino}/{nombre_archivo}"
        paginas = pdf_dict[archivo]
        textos = extraer_textos(nombre,ruta,paginas)
        for t in textos:
            lista_textos.append(t)
        print(f"{bcolors.BOLD}{bcolors.OKCYAN}Archivo {nombre_archivo} {bcolors.OKGREEN}escaneado{bcolors.ENDC}")

    print(f"{bcolors.BOLD}{bcolors.HEADER}{bcolors.UNDERLINE}\nDataFrame obtenido:{bcolors.ENDC}{bcolors.HEADER}{bcolors.BOLD}\nLegislatura {legislatura}\n{orador}\n{len(lista_textos)} intervenciones{bcolors.ENDC}")
    df = pd.DataFrame(lista_textos, columns =['Orador','Documento','Texto'])
    print(df)
    return df
    

recuperar_informacion('Sánchez Pérez-Castejón, Pedro',13,2)