def crear_html(tabla, ruta_ds, nombre_f):
    ruta_web = "./www/dataframe.html"

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel='stylesheet' href='{style}'>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <title>Visualización Dataframe</title>
</head>
<body>
    {encabezado}
    <div id="tabla_dinamica">
        {tabla_dinamica}
    </div>
    <div id="botonera">
        <div id="boton_ordenar">Ordenar por Documento <i class="fa-solid fa-file"></i></div>
        <div id="boton_modificar">Guardar modificaciones</div>
        <div id="boton_salir">Salir</div>
    </div>
</body>
<script src="{script}"></script>
</html>"""

    encabezado = f'<div id="encabezado"><p>Visualización del dataset <span>{ruta_ds}</span> en el archivo <span>{nombre_f}</span></p></div>'
    style = "{{ url_for('static', filename='css/style.css') }}"
    script = "{{ url_for('static', filename='js/script.js') }}"
    html_filled = html_content.format(tabla_dinamica=tabla, encabezado=encabezado, style=style, script=script)

    with open(ruta_web, 'w') as file:
        file.write(html_filled)