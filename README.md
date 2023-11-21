# Recopilador de Intervenciones en el Congreso

## Descripción

Simple programa para extraer y almacenar los fragmentos de texto de las transcripciones oficiales de los plenos en el Congreso.
Permite buscar las invervenciones de un determinado orador en cada legislatura. Almacena los fragmentos en un dataset dentro de un archivo HDF5.

## Requisitos Previos

Asegúrate de tener instalados:

- Python 3
- Make

## Instalación

Ejecuta el siguiente comando para clonar el repositorio en tu máquina.

```bash
git clone https://github.com/alediabre/recopilador-intervenciones-congreso.git
```


## Ejecutar el Programa

Puedes usar indistintamente usar el comando *make run* o sólamente *make*. Debes ejecutarlo desde la carpeta raíz.

```bash
cd recopilador-intervenciones-congreso
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

**Consideraciones**:

* Cuando se muestra en consola una lista de elementos numerados, se debe introducir por teclado el índice del elemento que queramos seleccionar.

* La **paginación** no asegura un determinado número de fragmentos, sólo es una medida orientativa. Cuanto mayor sea el parámetro *paginación* que introduzcamos, más fragmentos recopilaremos.

* En algunos casos las **legislaturas** más antiguas (1-10), presentan problemas debido a que la información se presenta de distinta forma. Se recomienda extraer información de las legislaturas más recientes.

* Los datasets se almacenan en archivos *.hdf5*. Se trata de archivos jerárquicos para gestionar y agrupar datasets. El programa da la opción de crear un nuevo archivo HDF o usar uno existente, concatenando los nuevos datos con los que había. En todo caso, se modificará el **Dataset** ***datos*** perteneciente al **Grupo** ***congreso***

* No siempre se recogen todas las intervenciones que hay en los PDF descargados. Las erratas en la transcripción, especialmente en los nombres, puede originar que se omitan fragmentos.

* Los fragmentos situados justo en el cierre de un PDF, pueden incluir algo más de texto de lo que realmente es la intervención del orador. Esto se debe a que no hay una forma adecuada de detectar el final de la intervención.


