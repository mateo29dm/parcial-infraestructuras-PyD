# Parcial de infraestructuras Paralelas y Distribuidas (Parte Practica)

Este repositorio se creo con el objetivo de cumplir con la parte practica de la entrega del parcial de la asignatura de Infraestructuras Paralelas y Distribuidas del a Universidad del Valle. 

## Integrantes 

Los integrantes que hicieron parte de la realizacion de este proyecto pertenecen a la Universidad del valle sede Melendez y cursan la carrera de Ingenieria de Sistemas

Integrantes:

- Deison Aleixer Cardona Arias, Codigo: 1840261, Correo: deison.cardona@correounivalle.edu.co
- Mateo Duque Millan, Codigo: 1843620, Correo: mateo.duque@correounivalle.edu.co

# Descripcion general del aplicativo

El aplicativo desarrollado se encarga de encontrar links de youtube proporcionados previamente en el codigo haciendo uso de la aplicacion yt-dlp, acto seguido extrae el audio de los videos mediante otra aplicacion llamada ffmpeg, y utiliza funciones auxiliares que con la ayuda de yt-dlp extraen infromacion y la plasman en un registro.csv, posteriormente elimina el video descargado dejando unicamente los audios y el registro.

# Descripcion de requerimientos

Para la utilizacion de este aplicativo es necesario tener instalados:
- **yt-dlp:** https://github.com/yt-dlp/yt-dlp
- **ffmpeg:** https://ffmpeg.org/

Estas dos herramientas son las que le dan la funcionalidad al aplicativo, conectan los links proporcionados con YouTube y extraen el audio de los videos descargados ademas de extraer informacion de los videos.
yt-dlp se encarga de todo lo relacionado con encontrar el video, descargarlo y extraer informacion de el mediante las funciones auxiliares implementadas en el aux_functions.py mientras que ffmpeg convierte los videos en audios .mp3, su llamada se hace en la funcion descargar_video_y_extraer_audio de cada uno de los archivos yt_audio_downloader.py en su version sequencial, multithreading o multiprocessing.

# Forma de Uso o ejecucion

El aplicativo se ejecuta como se ejecutaria cualquier programa de python desde la consola de comandos de Linux, en este caso el archivo a ejecutar seria el main.py ya que es el que conecta las 3 versiones del downloader
El comando recibe 2 argumentos que de no ser incluidos ejecutaran su valor por dejecto, estos argumentos son:
- **--modo:** Este argumento identifica el modo de ejecucion que desea el usuario, mt (Multithreading), mp (Multiprocessing) o sq (Sequential), y ejecutara la version del main correspondiente al archivo yt_audio_downloader del modo de ejecucion seleccionado. Por defecto ejecuta la version Sequential
- **--workers:** Este argumento se utiliza para especificar la cantidad de workers que el usuario desea utilizar para ejecutar la aplicacion, este valor solo tiene efecto en los modos de ejecucion Multithreading y Multiprocessing y su valor por defecto es 4.

Un ejemplo del comando de ejecucion:

``` python3 main.py --modo mp --hilos 16```

# Descripcion de la logica del aplicativo:

- **Importacion de modulos:** Se importan los modulos necesarios, en su mayoria son los mismos para los diferentes modos de ejecucion, los unicos modulos extra que se importan son el threading y el mutliprocessing en su respectivo archivo .py

- **Funcion main del archivo main.py:** Esta funcion se encarga de definir los argumentos que recibira el aplicativo por linea de comandos, de crear la lista con las url de los videos mediante la funcion auxiliar obtener_ultimos_videos y de decidir que archivo ejecutara en base al modo de ejecucion elegido. Del archivo escogido se ejecutara la funcion main respectiva y se le enviaran el numero de workers escogidos de ser necesario, y una lista de urls que se crea leyendo el archivo canales.json, en este archivo se encuentran las url de los canales seleccionados, una vez la funcion obtener_ultimos_videos extrae la url de cada canal utiliza la herramienta yt-dlp mediante linea de comandos para extraer los links de los videos de cada canal y guardarlos en una lista de urls misma que se utilizara como argumento para cada funcion main de cada modo.

- **Funcion main archivos yt_audio_downloader.py:** En el caso de la version Sequencial esta funcion hace uso de las funciones auxiliares para extraer el nombre del video y otra informacion para su posterior registro en el archivo registro.csv y ejecuta la eliminacion de los videos. Para el caso de las versiones multiprocessing y multithreading esta funcion utiliza un bucle que crea la cantidad de nucleos o hilos especificados por el usuario en la consola de comandos, cada una de estas unidades de procesamiento se encargara de ejecutar la funcion descargar_video_y_extraer_audio con sus respectivos argumentos, posteriormente inician la unidad de procesamiento y la agregan a su respectiva lista (threads en el caso de la version multithreading y processors en el caso de la version multiprocessing) despues espera a que terminan su trabajo para unir todas las unidades de procesamiento al hilo principal. En el caso de la version sequencial la funcion descargar_video_y_extraer_audio tambien es ejecutada pero tiene una ligera variacion.

- **Funcion descargar_video_y_extraer_audio:** Esta funcion se encarga de descargar el video y extraer el audio, para la version sequencial simplemente ejecuta la descarga de los videos utilizando la herramienta yt-dlp mediante la consola de comandos y extrae el audio con la herramienta ffmpeg tambien mediante la consola de comandos. En el caso de las versiones multiprocessing y multithreading utiliza un bucle para asignarle un grupo de urls a un hilo o nucleo y tambien se encarga de utilizar las funciones auxiliares para obtener informacion del video y registrarla en el archivo .csv, posteriormente utiliza un bucle while para asegurarse de que el archivo de audio ya fue creado y de ser cierto elimina el video descargado. Esta funcion utiliza la linea de comandos para ejecutar las herramientas yt-dlp y ffmpeg para descargar el video y extraer el audio respectivamente. Recibe los argumentos del identificador del hilo para utilizarlo como indice i esto sirve para que cada hilo empiece desde una url diferente, recibe la lista de urls para crear un rango desde i hasta el tamaño de la lista y para recorrerla en busca de las url respectivas, y recibe tambien el numero de hilos o nucleos para crear un salto correspondiente al numero de hilos o nucleos en el rango desde i hasta el tamaño de la lista de urls esto es para que cada hilo se encargue de procesar una url diferente hasta terminar la lista.

- **Funciones auxiliares del aux_funcions.py:** Todos los modos de ejecucion hacen uso de las funciones auxiliares presentes en el archivo aux_functions.py, este archivo hace uso de la herramienta yt_dlp para extraer informacion del video que le fue proporcionado mediante una url. Contiene 5 funciones: **registrar_descarga** que recibe la url y el nombre del video, registra la fecha de publicacion, fecha de descarga, nombre de video, url y nombre del canal en un archivo que crea llamado registro.csv, **obtener_fecha_publicacion** que mediante linea de comandos hace uso de la herramienta de yt-dlp para extraer la fecha de publicacion del video del url que recibe como argumento, **obtener_nombre_video** que mediante linea de comandos hace uso de la herramienta de yt-dlp para extraer el nombre del video del url que recibe como argumento, **obtener_nombre_canal** que mediante linea de comandos hace uso de la herramienta de yt-dlp para extraer el nombre del canal del url del video que recibe como argumento, y **obtener_ultimos_videos** que lee el archivo canales.json y mediante un bucle que recorre los canales guardados en el .json utiliza la linea de comandos y yt-dlp para extraer las id de las url de los 5 primeros videos que encuentra, estas id las guarda en una lista y mediante un bucle crea cada link de los videos y los guarda en la lista resultados, esta lista es retornada por la funcion.

# **Grafico de la logica del aplicativo**

**Logica general del aplicativo**

![Grafico de logica general](./app%20logic%20graph/Diagrama%20logica%20del%20aplicativo.png)

**Logica de ejecucion de paralelismo del aplicativo**

![Grafico de logica de procesos de paralelismo](./app%20logic%20graph/Parallel%20programming%20logic%20graph.png)

