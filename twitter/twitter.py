import pandas as pd
import os
import re
from getpass import getpass

from utils.colores_consola import bcolors
from twitter.webdriver import scraping,extraer_datos_tweets
from utils.dataset_handler import interaccion_usuario_dataset


def recuperar_informacion(my_user,my_pass,autor,num_max,fecha_ini,fecha_fin):
    '''
    Realiza todo el proceso de scraping, descarga de documentos y procesado de textos.
    Devuelve un Dataframe de pandas con todas las intervenciones que extrae para un orador en una legislatura (hasta la paginación dada)
    '''
    lista_tweets = []
    raw_tweets = scraping(autor,num_max,fecha_ini,fecha_fin,my_user,my_pass)
    for tweet in extraer_datos_tweets(autor,raw_tweets):
        lista_tweets.append((tweet[0], tweet[1], ''.join(tweet[2])))

    print(f"{bcolors.BOLD}{bcolors.HEADER}{bcolors.UNDERLINE}\nDataFrame obtenido:{bcolors.ENDC}{bcolors.HEADER}{bcolors.BOLD}\nAutor {autor}\nFecha de inicio {fecha_ini}\n{len(lista_tweets)} tweets\n{bcolors.ENDC}")
    df = pd.DataFrame(lista_tweets, columns =['Autor','Texto','Hashtags'])
    return df



async def inicio_twitter():

    ruta_ds = "/twitter/datos" #Ruta del Dataset (Grupo/Dataset) dentro del archivo HDF5
    ruta_data = "./data" #Ruta del directorio donde estarán los archivos HDF5
    max_num_tweets = 100 #Número máximo de tweets a extraer en cada procedimiento

    if os.path.isdir(ruta_data)==False:
        os.makedirs(ruta_data)

    #Mi usuario de Twitter----------------------------------------------------------------------------------
    my_user = input(f"{bcolors.WARNING}Introduzca su usuario de Twitter (el scrapping se realizará con dicho usuario): {bcolors.ENDC}")

    #Mi contraseña de Twitter----------------------------------------------------------------------------------
    my_pass = getpass(f"{bcolors.BOLD}Contraseña: {bcolors.ENDC}")

    #Seleccionar autor----------------------------------------------------------------------------------
    autor = input(f"{bcolors.BOLD}Introduzca el usuario del autor de los tweets: {bcolors.ENDC}")

    #Seleccionar numero de tweets-----------------------------------------------------------------------------------
    num_tweets = int(input(f"{bcolors.BOLD}Introduzca el número de tweets a extraer: {bcolors.ENDC}"))
    if num_tweets > max_num_tweets: num_tweets = max_num_tweets

    #Intervalo de fechas de los tweets-----------------------------------------------------------------------------------
    patron_fecha = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    fecha_ini = input(f"{bcolors.BOLD}Introduzca una fecha de inicio (YYYY-MM-DD): {bcolors.ENDC}")
    fecha_fin = input(f"{bcolors.BOLD}Introduzca una fecha de fin (YYYY-MM-DD): {bcolors.ENDC}")

    while not (patron_fecha.match(fecha_ini) or patron_fecha.match(fecha_fin)):
        print(f"{bcolors.WARNING}Formato de fechas incorrecto. Vuelva a intentarlo.\n{bcolors.ENDC}")
        fecha_ini = input(f"{bcolors.BOLD}Introduzca una fecha de inicio (YYYY-MM-DD): {bcolors.ENDC}")
        fecha_fin = input(f"{bcolors.BOLD}Introduzca una fecha de fin (YYYY-MM-DD): {bcolors.ENDC}")

    #Proceso de recuperar información y crear DataFrame-------------------------------------------------------
    dataframe = recuperar_informacion(my_user,my_pass,autor,num_tweets,fecha_ini,fecha_fin)

    if dataframe is not None:
        await interaccion_usuario_dataset(ruta_data, ruta_ds, dataframe)
    else:
        print(f"{bcolors.FAIL}Error al crear el Dataset. Vuelva a intentarlo.\n{bcolors.ENDC}")
   