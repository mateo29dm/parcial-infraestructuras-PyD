import subprocess
import os
import threading
from aux_functions import *

# Obtener la ruta del directorio actual del script
ruta_script = os.path.dirname(os.path.abspath(__file__))

# Cambiar al directorio del script
os.chdir(ruta_script)

def descargar_video_y_extraer_audio(ih, num_url, num_hilos, urls):

    for i in range(ih, num_url, num_hilos):
        nombre = obtener_nombre_video(urls[i])
        # Descargar el video
        subprocess.run(["yt-dlp", "-o", f"{nombre}", urls[i]])
    
        # Extraer el audio
        subprocess.run(["ffmpeg", "-i", f"{nombre}.webm", "-vn", "-codec:a", "libmp3lame", "-q:a", "0", f"./audiosMP/{nombre}.mp3"])

        # Crear el archivo .csv con el registro
        registrar_descarga(urls[i], nombre)


def main(num_hilos):
    # Lista de URLs de los videos a descargar
    urls = ["https://www.youtube.com/watch?v=4Fy6neJmX9s", "https://www.youtube.com/watch?v=XNwzxjB05fE", "https://www.youtube.com/watch?v=SQkFh8XOIcE", "https://www.youtube.com/watch?v=koX7Bua4WZs", "https://www.youtube.com/watch?v=5Ulf9ifvQPQ"]

    num_urls = len(urls)
    threads = []

    for i in range(num_hilos):
        thread = threading.Thread(target=descargar_video_y_extraer_audio, args=(i, num_urls, num_hilos, urls))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    print("Descarga completada!")