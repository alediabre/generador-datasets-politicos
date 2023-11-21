import h5py,tables
import pandas as pd
from utils.colores_consola import bcolors


def create_dataset(dataframe,ruta_ds):
    #Crear archivo de HDF5
    nombre_f = input(f"{bcolors.BOLD}Introduzca un nombre para el archivo (sin extensión): {bcolors.ENDC}")
    h5py.File("./data/"+nombre_f+".hdf5", "w")

    #Crear dataset en el archivo HDF5 con el dataframe de pandas
    dataframe.to_hdf("./data/"+nombre_f+".hdf5", ruta_ds)
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}El nuevo dataset se ha guardado en data/{nombre_f} ({ruta_ds}){bcolors.ENDC}")
    print(f'{bcolors.BOLD}{bcolors.HEADER}La forma del dataset es {dataframe.shape}{bcolors.ENDC}')


def read_dataframe(ruta_f,ruta_ds):
    f = pd.HDFStore(ruta_f)
    df = pd.read_hdf(f, ruta_ds)
    f.close()
    return df


def concatenate_dataframe(new_df,ruta_f,ruta_ds):
    f = pd.HDFStore(ruta_f)
    old_df = pd.read_hdf(f, ruta_ds)
    updated_df = pd.concat([old_df, new_df], ignore_index=True)
    f[ruta_ds] = updated_df
    f.close()
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}El dataset se ha actualizado en {ruta_f} ({ruta_ds}){bcolors.ENDC}")
    print(f'{bcolors.BOLD}{bcolors.HEADER}La forma del dataset ahora es {updated_df.shape}{bcolors.ENDC}')
