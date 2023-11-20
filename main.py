import pandas as pd
import os
import asyncio

from utils.colores_consola import bcolors
from utils.options import options_handler,list_options_handler
from docs import descargar_documentos
from webdriver import scraping,get_oradores
from text_parser import extraer_textos


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

    print(f"{bcolors.BOLD}{bcolors.HEADER}{bcolors.UNDERLINE}\nDataFrame obtenido:{bcolors.ENDC}{bcolors.HEADER}{bcolors.BOLD}\nLegislatura {legislatura}\n{orador}\n{len(lista_textos)} intervenciones\n{bcolors.ENDC}")
    df = pd.DataFrame(lista_textos, columns =['Orador','Documento','Texto'])

    return df



async def inicio():

    #Seleccionar legislatura----------------------------------------------------------------------------------
    legislatura = await list_options_handler(range(1,16),"Escriba el número de legislatura [1-15]: ",verbose=False)

    #Seleccionar orador---------------------------------------------------------------------------------------
    oradores = get_oradores(legislatura)
    orador_option = await list_options_handler(oradores,"\nSeleccione un orador de los anteriores (número):")
    orador = oradores[orador_option-1]

    #Seleccionar paginación-----------------------------------------------------------------------------------
    paginacion = int(input(f"{bcolors.BOLD}Introduzca la paginación máxima donde buscar: {bcolors.ENDC}"))

    #Proceso de recuperar información y crear DataFrame-------------------------------------------------------
    recuperar_informacion(orador,legislatura,paginacion)

    #Preguntar por guardado de DF-----------------------------------------------------------------------------
    ds_option = await options_handler(list("YyNn"),"¿Desea incorporar los datos obtenidos a un Dataset? [Y/N]",o0=list("Yy"),o1=list("Nn"))
    
    if ds_option == 0: #Si el usuario responde SI ("Y" o "y")
        print(f"{bcolors.BOLD}Mostrando datasets actuales\n{bcolors.ENDC}")
        datasets = os.listdir('./data')
        f_option = await list_options_handler(datasets,"Elija una opción: ",extra="Crear nuevo Dataset")

        if f_option == 0:
            print("Crear df")
            pass #Crear df
        else:
            ds = datasets[f_option-1]
            print(ds)
    else: pass 


if __name__ == "__main__":
    asyncio.run(inicio())