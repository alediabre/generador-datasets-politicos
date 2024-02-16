import os
from flask import Flask, request, jsonify, render_template
import logging

from utils.colores_consola import bcolors
from utils.input_handler import list_options_handler, options_handler
from utils.dataset_handler import read_dataframe, drop_rows_dataframe, generate_document
from utils.template_congreso import crear_html_congreso
from utils.template_twitter import crear_html_twitter                                                                                                                                                                                                                                                                    


app = Flask(__name__, template_folder='../www', static_folder='../www/static')
app.config["TEMPLATES_AUTO_RELOAD"] = True #Cuando se recarga la página, se carga el html actualizado

ruta_data = "./data" #Ruta del directorio donde estarán los archivos HDF5
ruta_ds, nombre_f = '',''


@app.route('/congreso')
def index_congreso():
    df = read_dataframe(ruta_data+"/"+nombre_f, ruta_ds)
    crear_html_congreso(df.to_html(), ruta_ds, nombre_f)
    return render_template('dataframe_congreso.html')


@app.route('/twitter')
def index_twitter():
    df = read_dataframe(ruta_data+"/"+nombre_f, ruta_ds)
    crear_html_twitter(df.to_html(), ruta_ds, nombre_f)
    return render_template('dataframe_twitter.html')


@app.route('/deleteRows', methods=['POST'])
def deleteRows():
    data = request.json
    filas = data.get('filas')
    if not filas:
        return jsonify({"success": False, "message": "No se proporcionaron filas para eliminar"})
    
    drop_rows_dataframe(filas, ruta_data+"/"+nombre_f, ruta_ds)
    return jsonify({ "success": True, "message": "El dataset ha sido modificado." })


@app.route('/createDoc', methods=['POST'])
def createDoc():
    if os.path.isdir('./documents')==False:
        os.makedirs('./documents')
    data = request.json
    dataset = data.get('dataset')
    generate_document(ruta_data,nombre_f[:-5],dataset)
    return jsonify({ "success": True, "message": "Se ha generado un documento con el dataset en la ruta ./documents" })
    


async def inicio_visualizacion():
    global ruta_data,nombre_f,ruta_ds

    print(f"{bcolors.BOLD}\nArchivos disponibles:\n{bcolors.ENDC}")
    data_files = os.listdir(ruta_data)
    f_option = await list_options_handler(data_files,"Indique un archivo: ")
    nombre_f = data_files[f_option-1]

    tipo = await options_handler(list("TtCc"),"Ver datos de Twitter [T] o ver datos del Congreso [C] ",list("Tt"),list("Cc"))
    if tipo == 0: visualizacion = "twitter"
    else: visualizacion= "congreso"

    ruta_ds = "/"+visualizacion+"/datos"
    
    log = logging.getLogger('werkzeug')
    log.disabled = True #Servidor flask no verboso

    print(f"{bcolors.BOLD}{bcolors.WARNING}\nAbra el navegador en 'http://localhost:5000/{visualizacion}' para la visualización. Para finalizar pulse CTRL+C{bcolors.ENDC}")
    app.run()
