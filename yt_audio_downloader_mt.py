import subprocess
import os
import threading
import time
from aux_functions import *

def descargar_video_y_extraer_audio(ih, num_hilos, urls):

    for i in range(ih, len(urls), num_hilos):
        nombre = obtener_nombre_video(urls[i])
        # Descargar el video
        subprocess.run(["yt-dlp", "-o", f"{nombre}", urls[i]])
    
        # Extraer el audio
        subprocess.run(["ffmpeg", "-i", f"{nombre}.webm", "-vn", "-codec:a", "libmp3lame", "-q:a", "0", f"./audiosMT/{nombre}.mp3"])

        # Crear el archivo .csv con el registro
        registrar_descarga(urls[i], nombre)

        while not os.path.exists(f"./audiosMT/{nombre}.mp3"):
            time.sleep(0.000000001)

        os.remove(f"{nombre}.webm")
            


def main(urls, num_hilos):
    
    threads = []

    for i in range(num_hilos):
        thread = threading.Thread(target=descargar_video_y_extraer_audio, args=(i, num_hilos, urls))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    print("Descarga completada!")