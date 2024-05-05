import subprocess
import subprocess
import os
import timeit
from aux_functions import *

def descargar_video_y_extraer_audio(url, nombre):
    # Extraccion del nombre del video
    nombre = obtener_nombre_video(url)

    # Descargar el video
    subprocess.run(["yt-dlp", "-o", f"{nombre}", url])
    
    # Extraer el audio
    subprocess.run(["ffmpeg", "-i", f"{nombre}.webm", "-vn", "-codec:a", "libmp3lame", "-q:a", "0", f"./audiosSQ/{nombre}.mp3"])

    


def main(urls, tiempo_inicializacion):

    start = timeit.default_timer()

    for url in urls:
        # Extraccion del nombre del video
        nombre = obtener_nombre_video(url)
        # Descarga del video y extraccion de audio
        descargar_video_y_extraer_audio(url, nombre)
        # Creacion y registro de los datos del video en el archivo registro.csv
        registrar_descarga(url, nombre)
        # Eliminar el video
        os.remove(f"{nombre}.webm")

    end = timeit.default_timer()
    
    tiempo_procesamiento = end - start

    print("Descarga completada!")
    print (f"Tiempo en inicializacion = {tiempo_inicializacion}")
    print(f"Tiempo en procesamiento = {tiempo_procesamiento}")
    print(f"Tiempo total {tiempo_inicializacion + tiempo_procesamiento}")