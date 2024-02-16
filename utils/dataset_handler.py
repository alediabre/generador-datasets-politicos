import os,h5py,tables
import pandas as pd
from utils.colores_consola import bcolors
from utils.input_handler import options_handler,list_options_handler


def create_dataset(dataframe,ruta_ds):
    ruta_data = './data'
    #Crear archivo de HDF5
    nombre_f = input(f"{bcolors.BOLD}Introduzca un nombre para el archivo (sin extensión): {bcolors.ENDC}")
    h5py.File(ruta_data+"/"+nombre_f+".hdf5", "w")

    #Crear dataset en el archivo HDF5 con el dataframe de pandas
    dataframe.to_hdf(ruta_data+"/"+nombre_f+".hdf5", ruta_ds)
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}El nuevo dataset se ha guardado en {ruta_data}/{nombre_f} ({ruta_ds}){bcolors.ENDC}")
    print(f'{bcolors.BOLD}{bcolors.HEADER}La forma del dataset es {dataframe.shape}{bcolors.ENDC}')


def read_dataframe(ruta_f,ruta_ds):
    f = pd.HDFStore(ruta_f)
    df = pd.read_hdf(f, ruta_ds)
    f.close()
    return df

def drop_rows_dataframe(rows,ruta_f,ruta_ds):
    f = pd.HDFStore(ruta_f)
    df = pd.read_hdf(f, ruta_ds)
    updated_df = df.drop(rows)
    f[ruta_ds] = updated_df
    f.close()

def concatenate_dataframe(new_df,ruta_f,ruta_ds):
    f = pd.HDFStore(ruta_f)
    try:
        old_df = pd.read_hdf(f, ruta_ds)
        updated_df = pd.concat([old_df, new_df], ignore_index=True)
        f[ruta_ds] = updated_df
        f.close()
        print(f"{bcolors.BOLD}{bcolors.OKGREEN}El dataset se ha actualizado en {ruta_f} ({ruta_ds}){bcolors.ENDC}")
        print(f'{bcolors.BOLD}{bcolors.HEADER}La forma del dataset ahora es {updated_df.shape}{bcolors.ENDC}')
    except KeyError: #Si no existe el dataset (sea de congreso o twitter) en dicho archivo, lo crea
        new_df.to_hdf(ruta_f, ruta_ds)


def generate_document(ruta_data,nombre_f,dataset):
    ruta_f = ruta_data+"/"+nombre_f
    ruta_ds = "/"+dataset+"/datos"
    f = pd.HDFStore(ruta_f)
    df = pd.read_hdf(f, ruta_ds)
    with open('./documents/'+nombre_f+'_'+dataset+'.txt', 'w') as doc:
        for _, fila in df.iterrows():
            doc.write(fila['Texto'] + '\n\n')
    f.close()


async def interaccion_usuario_dataset(ruta_data, ruta_ds, dataframe):
    '''
    Maneja la interacción del usuario en la terminal para el guardado de dataframes.
    Primero pregunta por guardar o descartar.
    En caso de guardar, pregunta por seleccionar un archivo hdf dentro de ruta_data o crear uno nuevo. 
    Si se selecciona uno existente, se concatena el dataframe con el que ya existía en dicho dataset
    '''
    dataset_option = await options_handler(list("YyNn"),"¿Desea incorporar los datos obtenidos a un Dataset? [Y/N]",list("Yy"),list("Nn"))
    
    if dataset_option == 0: #Si el usuario responde SI ("Y" o "y")
        print(f"{bcolors.BOLD}Mostrando archivos HDF5 actuales\n{bcolors.ENDC}")
        data_files = os.listdir(ruta_data)
        file_option = await list_options_handler(data_files,"Elija una opción: ",extra="Crear nuevo archivo")

        if file_option == 0: #Si el usuario decide crear nuevo archivo
            create_dataset(dataframe,ruta_ds)

        else: #Si el usuario decide concatenar el df sobre otro archivo
            nombre_f = data_files[file_option-1]
            concatenate_dataframe(dataframe, ruta_data+"/"+nombre_f, ruta_ds) #Concatena con lo que había en el dataset y lo guarda
    else:
        print(f"{bcolors.BOLD}Se ha descartado el Dataframe{bcolors.ENDC}")