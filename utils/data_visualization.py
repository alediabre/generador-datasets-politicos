import os

from utils.colores_consola import bcolors
from utils.input_handler import list_options_handler, options_handler
from utils.dataset_handler import read_dataframe


async def inicio_visualizacion():

    ruta_data = "./data" #Ruta del directorio donde estarán los archivos HDF5

    print(f"{bcolors.BOLD}\nArchivos disponibles:\n{bcolors.ENDC}")
    data_files = os.listdir(ruta_data)
    f_option = await list_options_handler(data_files,"Indique un archivo: ")
    nombre_f = data_files[f_option-1]

    tipo = await options_handler(list("TtCc"),"Ver datos de Twitter [T] o ver datos del Congreso [C] ",list("Tt"),list("Cc"))
    if tipo == 0:
        ruta_ds = "/twitter/datos"
    else: ruta_ds= "/congreso/datos"

    df = read_dataframe(ruta_data+"/"+nombre_f, ruta_ds)
    print(df)