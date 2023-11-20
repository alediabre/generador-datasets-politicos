import shutil,os,requests
from colores_consola import bcolors


def descargar_documentos(pdf_dict,carpeta_destino):
    '''
    Descarga los pdf dados por "pdf_dict" y los guarda en un directorio. Destruye el directorio con los pdf anteriores.
    Nombra los archivos pdf en base a su enlace.
    '''

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