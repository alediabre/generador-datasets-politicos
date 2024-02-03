import pandas as pd
import os

from utils.colores_consola import bcolors
from utils.input_handler import list_options_handler
from utils.dataset_handler import interaccion_usuario_dataset
from congreso.docs import descargar_documentos
from congreso.webdriver import scraping,get_oradores
from congreso.text_parser import extraer_textos


def recuperar_informacion(orador,legislatura,paginacion):
    '''
    Realiza todo el proceso de scraping, descarga de documentos y procesado de textos.
    Devuelve un Dataframe de pandas con todas las intervenciones que extrae para un orador en una legislatura (hasta la paginación dada)
    '''

    lista_textos = []
    pdf_dict = scraping(orador,legislatura,paginacion)
    carpeta_destino = "./pdf"
    descargar_documentos(pdf_dict,carpeta_destino)

    nombre = orador.split(',')[0].upper()
    for archivo in pdf_dict:

        nombre_archivo = archivo.split('oficiales/')[1].replace('/','_')
        ruta = f"{carpeta_destino}/{nombre_archivo}"

        file_exists = os.path.isfile(ruta) #Evita errores si el archivo no se descargó
        if file_exists:
            paginas = pdf_dict[archivo]
            textos = extraer_textos(nombre,ruta,paginas)
            for t in textos:
                lista_textos.append(t)
            print(f"{bcolors.BOLD}{bcolors.OKCYAN}Archivo {nombre_archivo} {bcolors.OKGREEN}escaneado{bcolors.ENDC}")

    print(f"{bcolors.BOLD}{bcolors.HEADER}{bcolors.UNDERLINE}\nDataFrame obtenido:{bcolors.ENDC}{bcolors.HEADER}{bcolors.BOLD}\nLegislatura {legislatura}\n{orador}\n{len(lista_textos)} intervenciones\n{bcolors.ENDC}")
    df = pd.DataFrame(lista_textos, columns =['Orador','Documento','Texto'])
    return df



async def inicio_congreso():

    ruta_ds = "/congreso/datos" #Ruta del Dataset (Grupo/Dataset) dentro del archivo HDF5
    ruta_data = "./data" #Ruta del directorio donde estarán los archivos HDF5

    if os.path.isdir(ruta_data)==False:
        os.makedirs(ruta_data)

    #Seleccionar legislatura----------------------------------------------------------------------------------
    legislatura = await list_options_handler(range(1,16),"Escriba el número de legislatura [1-15]: ",verbose=False)

    #Seleccionar orador---------------------------------------------------------------------------------------
    oradores = get_oradores(legislatura)
    orador_option = await list_options_handler(oradores,"\nSeleccione un orador de los anteriores (número):")
    orador = oradores[orador_option-1]

    #Seleccionar paginación-----------------------------------------------------------------------------------
    paginacion = int(input(f"{bcolors.BOLD}Introduzca la paginación máxima donde buscar: {bcolors.ENDC}"))

    #Proceso de recuperar información y crear DataFrame-------------------------------------------------------
    dataframe = recuperar_informacion(orador,legislatura,paginacion)

    await interaccion_usuario_dataset(ruta_data, ruta_ds, dataframe)