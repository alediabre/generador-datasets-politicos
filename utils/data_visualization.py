import os, signal
from flask import Flask, jsonify, render_template
import logging
import webbrowser, threading

from utils.colores_consola import bcolors
from utils.input_handler import list_options_handler, options_handler
from utils.dataset_handler import read_dataframe
from utils.template_creator import crear_html                                                                                                                                                                                                                                                                                                        


app = Flask(__name__, template_folder='../www', static_folder='../www/static')


def open_browser():
    webbrowser.open('http://localhost:5000', new=2)

@app.route('/')
def index():
    return render_template('dataframe.html')

@app.route('/stopServer', methods=['POST'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "El servidor está desconectado." })

@app.route('/deleteRows', methods=['POST'])
def deleteRows():

    return jsonify({ "success": True, "message": "El dataset ha sido modificado." })




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
    
    log = logging.getLogger('werkzeug')
    log.disabled = True #Servidor flask no verboso

    browser_thread = threading.Timer(1, open_browser)
    browser_thread.start()
    app.run()
    browser_thread.join()
    
    print("aaa")
