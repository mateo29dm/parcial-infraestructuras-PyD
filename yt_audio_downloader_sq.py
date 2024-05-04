import subprocess
import subprocess
import os
from aux_functions import *

def descargar_video_y_extraer_audio(url, nombre):
    # Extraccion del nombre del video
    nombre = obtener_nombre_video(url)

    # Descargar el video
    subprocess.run(["yt-dlp", "-o", f"{nombre}", url])
    
    # Extraer el audio
    subprocess.run(["ffmpeg", "-i", f"{nombre}.webm", "-vn", "-codec:a", "libmp3lame", "-q:a", "0", f"./audiosSQ/{nombre}.mp3"])


def main():
    # Lista de URLs de los videos a descargar
    urls = ["https://www.youtube.com/watch?v=4Fy6neJmX9s", "https://www.youtube.com/watch?v=XNwzxjB05fE",
            "https://www.youtube.com/watch?v=SQkFh8XOIcE", "https://www.youtube.com/watch?v=koX7Bua4WZs",
            "https://www.youtube.com/watch?v=5Ulf9ifvQPQ"]

    for url in urls:
        # Extraccion del nombre del video
        nombre = obtener_nombre_video(url)
        # Descarga del video y extraccion de audio
        descargar_video_y_extraer_audio(url, nombre)
        # Creacion y registro de los datos del video en el archivo registro.csv
        registrar_descarga(url, nombre)
        # Eliminar el video
        os.remove(f"{nombre}.webm")