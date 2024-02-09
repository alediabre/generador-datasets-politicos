# Generador de Datasets de Discursos Políticos

## Descripción

Simple programa para extraer y almacenar discursos políticos de dos fuentes: Congreso de los Diputados y Twitter. 
Recopila los tweets de un usuario dado entre dos fechas.
Recopila los fragmentos de texto de las transcripciones oficiales de los plenos en el Congreso.
Permite buscar las invervenciones de un determinado orador en cada legislatura. 
Almacena los fragmentos en un dataset dentro de un archivo HDF5 y permite filtrarlos de forma visual y sencilla para limpiar el dataset.

## Requisitos Previos

Asegúrate de tener instalados:

- Python 3
- Make

## Instalación

Ejecuta el siguiente comando para clonar el repositorio en tu máquina.

```bash
git clone https://github.com/alediabre/generador-datasets-politicos.git
```


## Ejecutar el Programa

Puedes usar indistintamente usar el comando *make run* o sólamente *make*. Debes ejecutarlo desde la carpeta raíz.

```bash
cd generador-datasets-politicos
```
```bash
make run
```
```bash
make
```

## Configuración del Entorno Virtual

Para evitar conflictos con las dependencias del sistema, se usa un entorno virtual para la ejecución. Se configura automáticamente al ejecutar el programa con *make*. Se reinstalarán las dependencias si hay cambios en el fichero **requirements.txt**

## Limpiar el directorio

Este comando eliminará los archivos generados por el programa y el entorno virtual.

```bash
make clean
```

## Manual de uso

El programa te irá guiando paso a paso. Sigue las instrucciones que te proporciona y en algunos casos ten paciencia.

**Consideraciones Congreso**:

* Cuando se muestra en consola una lista de elementos numerados, se debe introducir por teclado el índice del elemento que queramos seleccionar.

* La **paginación** no asegura un determinado número de fragmentos, sólo es una medida orientativa. Cuanto mayor sea el parámetro *paginación* que introduzcamos, más fragmentos recopilaremos.

* En algunos casos las **legislaturas** más antiguas (de la 1 a la 10), presentan problemas debido a que la información se presenta de distinta forma. Se recomienda extraer información de las legislaturas más recientes.

* Los datasets se almacenan en archivos *.hdf5*. Se trata de archivos jerárquicos para gestionar y agrupar datasets. El programa da la opción de crear un nuevo archivo HDF o usar uno existente, concatenando los nuevos datos con los que había. En todo caso, se modificará el **Dataset** ***datos*** perteneciente al **Grupo** ***congreso***

* No siempre se recogen todas las intervenciones que hay en los PDF descargados. Las erratas en la transcripción, especialmente en los nombres, puede originar que se omitan fragmentos.

* Los fragmentos situados justo en el cierre de un PDF, pueden incluir algo más de texto de lo que realmente es la intervención del orador. Esto se debe a que no hay una forma adecuada de detectar el final de la intervención.


**Consideraciones Twitter**:

* Se debe introducir un nombre de usuario y contraseña personales con el que el bot realizara el proceso de recopilación de tweets.

* Por seguridad recomienda usar una cuenta nueva de Twitter/X para este proceso, y no realizar demasiadas peticiones de forma muy continuada, ya que existe el riesgo de suspensión de la cuenta por actividad fuera de lo normal.

* Los tweets comenzarán a recopilarse en orden cronológico desde la fecha de inicio dada, hasta la fecha de fin, como máximo. Si antes de llegar a dicha fecha se alcanza el número de tweets a extraer indicado, se para el proceso.

* El número de tweets a extraer cada vez que se realiza el proceso, está limitado a 100 por seguridad, el proceso se puede repetir sin límites, bajo la responsabilidad del usuario.

* Es posible que no se alcance el número deseado de tweets, debido a que algunos sean publicidad, y en ese caso se descartan automáticamente.


**Editor de Datasets**:

En el editor podemos visualizar el dataset de Twitter o el dataset del Congreso, de un determinado archivo hdf5. Podemos ordenar las filas por distintos parámetros (o varios a la vez), y filtrar por el número de palabras que contenga el texto. También es posible buscar palabras o frases concretas en el buscador, que funciona como otro filtro.

Se puede ampliar el texto para leerlo al completo haciendo click en una celda, y copiar al portapapeles en la columna asignada a ello. Si eliminamos una fila, se deben guardar las modificaciones para que el cambio se efectúe en el archivo y perdure.

Con estas herramientas es posible encontrar textos con ciertas carácterísticas rápidamente, para filtrar datos no deseados y limpiar el dataset.


