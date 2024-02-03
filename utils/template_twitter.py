def crear_html_twitter(tabla, ruta_ds, nombre_f):
    ruta_web = "./www/dataframe_twitter.html"

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' href="{style_general}">
    <link rel='stylesheet' href="{style_twitter}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <title>Visualización Dataframe</title>
</head>
<body>
    {encabezado}
    <div id="filtros">
        <input type="text" id="buscadorTexto" data-columna="1" placeholder="Busca cualquier texto..." title="Escribe un fragmento">
        <div class="slidecontainer">
            <input type="range" min="1" max="150" value="150" class="slider" id="rangoPalabras" data-columna="1">
            <p>Palabras: <span id="numPalabras"></span></p>
        </div>
        <div class="info">
            <p>Nº Elementos: <span></span></p>
            <p>Nº Autores: <span></span></p>
        </div>
    </div>
    <div id="tabla_dinamica">
        {tabla_dinamica}
    </div>
    <div id="botonera">
        <div id="boton_ordenar">Ordenar por Autor <i class="fa-solid fa-user"></i></div>
        <div id="boton_modificar">Guardar modificaciones <span>0</span></div>
        <div id="boton_salida">Generar documentos</div>
    </div>
</body>
<script>window.contexto = 'twitter'</script>
<script type="module" src="{script}"></script>
</html>"""

    encabezado = f'<div id="encabezado"><p>Visualización del dataset <span>{ruta_ds}</span> en el archivo <span>{nombre_f}</span></p></div>'
    style_general = "{{ url_for('static', filename='css/styles_editor.css') }}"
    style_twitter = "{{ url_for('static', filename='css/styles_twitter.css') }}"
    script = "{{ url_for('static', filename='js/editor.js') }}"
    html_filled = html_content.format(tabla_dinamica=tabla, encabezado=encabezado, style_general=style_general,style_twitter=style_twitter, script=script)

    with open(ruta_web, 'w') as file:
        file.write(html_filled)