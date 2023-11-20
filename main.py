import pandas as pd

from colores_consola import bcolors
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

    print(f"{bcolors.BOLD}{bcolors.HEADER}{bcolors.UNDERLINE}\nDataFrame obtenido:{bcolors.ENDC}{bcolors.HEADER}{bcolors.BOLD}\nLegislatura {legislatura}\n{orador}\n{len(lista_textos)} intervenciones{bcolors.ENDC}")
    df = pd.DataFrame(lista_textos, columns =['Orador','Documento','Texto'])
    print(df)
    return df



def inicio():

    legislatura = int(input(f"{bcolors.BOLD}Escriba el número de legislatura: {bcolors.ENDC}"))

    options_oradores = get_oradores(legislatura)
    for i,option in enumerate(options_oradores):
        print(f'{bcolors.BOLD}{bcolors.OKCYAN}{i+1} {option}{bcolors.ENDC}')

    num_option = int(input(f'{bcolors.BOLD}\nSeleccione un orador de los anteriores (número): {bcolors.ENDC}'))
    orador = options_oradores[num_option-1]

    paginacion = int(input(f"{bcolors.BOLD}Introduzca la paginación máxima donde buscar: {bcolors.ENDC}"))

    recuperar_informacion(orador,legislatura,paginacion)


if __name__ == "__main__":
    inicio()
    #recuperar_informacion('Sánchez Pérez-Castejón, Pedro',13,2)