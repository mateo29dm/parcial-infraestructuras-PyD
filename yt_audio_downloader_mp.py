import subprocess
import os
import multiprocessing
import time
from aux_functions import *

def descargar_video_y_extraer_audio(ih, num_nucleos, urls):

    for i in range(ih, len(urls), num_nucleos):
        nombre = obtener_nombre_video(urls[i])
        # Descargar el video
        subprocess.run(["yt-dlp", "-o", f"{nombre}", urls[i]])
    
        # Extraer el audio
        subprocess.run(["ffmpeg", "-i", f"{nombre}.webm", "-vn", "-codec:a", "libmp3lame", "-q:a", "0", f"./audiosMP/{nombre}.mp3"])

        # Crear el archivo .csv con el registro
        registrar_descarga(urls[i], nombre)

        while not os.path.exists(f"./audiosMP/{nombre}.mp3"):
            time.sleep(0.000000001)

        os.remove(f"{nombre}.webm")
            


def main(urls, num_nucleos):

    processors = []

    for i in range(num_nucleos):
        nucleo = multiprocessing.Process(target=descargar_video_y_extraer_audio, args=(i, num_nucleos, urls))
        nucleo.start()
        processors.append(nucleo)
    
    for nucleo in processors:
        nucleo.join()

    print("Descarga completada!")