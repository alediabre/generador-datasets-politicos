import re
import pdfplumber

from utils.colores_consola import bcolors


def extraer_textos(orador, ruta, paginas):
    '''
    Recibe el orador en formato correcto (Mayúsculas, solo los apellidos)
    Recibe la ruta del documento pdf
    Recibe las páginas que contienen las intervenciones
    Devuelve una lista de fragmentos extraídos con la siguiente forma (orador, nombre del documento, fragmento)
    AVISO: Puede que se ingoren algunas intervenciones si en el documento los nombres contienen alguna errata

    Para la extracción se siguen las siguientes reglas:
    Regla1: Comenzar tras el primer ":" después del orador en mayúscula (o en minúsculas entre paréntesis)
    Regla2: Terminar en la línea anterior al siguiente nombre en negrita y mayúscula
    Regla3: Eliminar contenido entre paréntesis y saltos de línea
    '''
    lista_fragmentos = []
    num_paginas = len(paginas)
    left,top,right,bottom = 50.0,100.0,550.0,780.0

    def comenzar_fragmento(texto,vista):
        '''
        Para encontrar el inicio, busca: 
        a) El nombre del orador en mayúsculas. 
        b) El nombre del orador en minúsculas (primera letra mayúscula) entre paréntesis, tras una palabra mayúscula
        Si la pagina ha sido vista antes X veces, se toma la aparición número X
        Devuelve el texto acotado desde el inicio del fragmento en adelante
        '''
        orador_en_parentesis = orador.title()
        matches_inicio = list(re.finditer(rf'{orador}.*:|[A-Z]\w+[A-Z](\s[0-9]*)?\s\({orador_en_parentesis}\):', texto))
        if len(matches_inicio)>vista:
            #print(matches_inicio[vista])
            return texto[matches_inicio[vista].end():].strip()
        else: return False
        
    def esNegrita(palabra,cadena,caracteres):
        '''
        Devuelve True si una palabra está en negrita en el pdf.
        Para ello comprueba la propiedad 'fontname' del primer caracter de la palabra.
        El primer índice del primer caracter en "caracteres" se obtiene buscando la palabra en cadena (la concatenacion de caracteres)
        '''
        match_palabra = re.search(palabra, cadena)
        first_char = caracteres[match_palabra.start()]
        if "Bold" in first_char["fontname"]:
            return True
        else: return False
            
    def terminar_fragmento(texto,cadena,caracteres):
        '''
        Para encontrar el final del fragmento va recorriendo las palabras mayúsculas hasta encontrar una en negrita.
        Devuelve el fragmento, acabado en el salto de línea justamente previo a la palabra encontrada.
        '''
        matches = re.finditer(r'(^|\n).*([A-Z]\w+[A-Z])',texto)
        for match_fin in matches:
            palabra = match_fin.group(2)
            if esNegrita(palabra,cadena,caracteres):
                return texto[:match_fin.start()]
        return False
    
    def crop_page(pagina,x0,top,x1,bottom):
        '''
        Recorta la pagina de forma que solo incluya el texto relevante, sin la cabecera o el código lateral. Usa coordenadas
        '''
        my_bbox = (x0,top,x1,bottom)
        page_crop = pagina.crop(bbox=my_bbox)
        return page_crop

    
    with pdfplumber.open(ruta) as pdf:

        pagina_anterior = False #Contenido de la página anterior para el actual fragmento. False si no lo hay
        vista = 0 #Numero de veces que se ha buscado en la página actual
        p_origen = paginas[0] #Primera página en la pila de páginas, de la que se parte para extraer un fragmento
        p = p_origen #Variable para iterar sobre la primera página de la pila, hasta encontrar el final del fragmento

        def avanzar_pagina():
            '''
            Se elimina la página más alta en la pila actualmente y se actualiza la variable "p_origen" con la nueva página más alta.
            Incrementa el numero de vistas si la página es la misma que la recientemente vista (hay una múltiple intervención).
            En caso de ser una página distinta a la anterior, vista=0
            Si sólo queda una página, se elimina de la pila y no se actualizan variables.
            '''
            nonlocal p_origen, p, vista
            if len(paginas) > 1:
                vista = vista+1 if paginas[0] == paginas[1] else 0
                paginas.remove(p_origen)
                p_origen = paginas[0]
                p = p_origen
            else: paginas.remove(p_origen)

        #Se repite el proceso mientras no se acabe la pila de páginas
        while len(paginas)>0: 

            print(f'{bcolors.BOLD}Página: {num_paginas-len(paginas)}/{num_paginas}{bcolors.ENDC}', end='\r') #Imprime el progreso de paginas
            pagina = pdf.pages[p-1]
            pagina_recortada = crop_page(pagina,left,top,right,bottom)
            texto = pagina_recortada.extract_text()   #Texto normal de la pagina
            caracteres = pagina_recortada.chars   #Lista de caracteres de la pagina con sus propiedades
            cadena = "".join(c['text'] for c in caracteres) #Encadenamiento de los caracteres. Aqui las letras tienen los mismos índices que en "caracteres"

            #Si no hay pagina anterior, se busca la cota inicial. Si la hay, la cota es toda la pagina
            if pagina_anterior == False: 
                cota_fragmento = comenzar_fragmento(texto,vista)
            else:
                cota_fragmento = texto

            #Si no hay cota en la página prevista(no se encuentra el nombre, suele ser por errata) -> Se avanza página
            if cota_fragmento == False: 
                pagina_anterior = False
                avanzar_pagina()
            else:
                #En caso contrario buscamos el final del fragmento a partir de la cota
                fragmento = terminar_fragmento(cota_fragmento,cadena,caracteres)

                #Si no se ha encontrado el final de la intervención en la página actual, se pasa a la siguiente página y se añade la cota actual a "pagina_anterior"
                #p debe no ser la última página, para llevar a cabo este paso.
                if fragmento == False and len(pdf.pages)>p:
                    pagina_anterior = pagina_anterior+cota_fragmento if pagina_anterior != False else cota_fragmento
                    p+=1
                else: 
                    #En caso de terminar el fragmento en la página actual
                    #Si hay parte del fragmento en la pagina anterior, se juntan, y se restablece a False "pagina_anterior"
                    if pagina_anterior != False:
                        fragmento = pagina_anterior+fragmento
                        pagina_anterior = False

                    fragmento = cota_fragmento if len(pdf.pages)<=p else fragmento #Si no hay fragmento porque es la ultima página, pasa a serlo la cota entera

                    #Limpiar fragmento -> Eliminar paréntesis y el punto si lo precede. Eliminar saltos de linea
                    fragmento_limpio = re.sub(r'\n',' ',re.sub(r'\.\s\([^\(]*\)|\([^\(]*\)', '', fragmento))
                    nombre_doc = ruta.split("/")[2].split(".")[0]
                    #Crear entrada para la lista de fragmentos y avanzar página
                    lista_fragmentos.append((orador,nombre_doc,fragmento_limpio))
                    avanzar_pagina()

    return lista_fragmentos