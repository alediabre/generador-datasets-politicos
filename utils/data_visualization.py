import os
import webbrowser

from utils.colores_consola import bcolors
from utils.input_handler import list_options_handler, options_handler
from utils.dataset_handler import read_dataframe


def crear_html(tabla, ruta_ds, nombre_f):
    ruta_web = "./www/dataframe.html"

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Visualización Dataframe</title>
</head>
<body>
    {encabezado}
    <div id="tabla_dinamica">
        {tabla_dinamica}
    </div>
</body>
<script src="script.js"></script>
</html>"""

    encabezado = f'<div id="encabezado"><p>Visualización del dataset <span>{ruta_ds}</span> en el archivo <span>{nombre_f}</span></p></div>'
    html_filled = html_content.format(tabla_dinamica=tabla, encabezado=encabezado)

    with open(ruta_web, 'w') as file:
        file.write(html_filled)





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
    crear_html(df.to_html(), ruta_ds, nombre_f)

    path = os.path.abspath("./www/dataframe.html")
    url = f'file:///{path}'
    webbrowser.open(url, new=2)