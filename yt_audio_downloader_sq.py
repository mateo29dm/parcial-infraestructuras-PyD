import subprocess
import csv
import datetime
import subprocess
import json
import os

# Obtener la ruta del directorio actual del script
ruta_script = os.path.dirname(os.path.abspath(__file__))

# Cambiar al directorio del script
os.chdir(ruta_script)

def descargar_video_y_extraer_audio(url, nombre):

    # Descargar el video
    subprocess.run(["yt-dlp", "-o", f"{nombre}", url])
    
    # Extraer el audio
    subprocess.run(["ffmpeg", "-i", f"{nombre}.webm", "-vn", "-codec:a", "libmp3lame", "-q:a", "0", f"./audiosSQ/{nombre}.mp3"])

def registrar_descarga(canal, url, nombre):
    fecha_descarga = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_publicacion = obtener_fecha_publicacion(url)  # Debes implementar esta función
    with open("registro.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([canal, nombre, url, fecha_publicacion, fecha_descarga])


def obtener_fecha_publicacion(url):
    # Obtener la información del video utilizando yt-dlp en formato JSON
    resultado = subprocess.run(["yt-dlp", "-J", url], capture_output=True, text=True)
    info_video = json.loads(resultado.stdout)
    
    # Obtener la fecha de publicación del video del JSON
    fecha_publicacion = info_video.get("upload_date")
    fecha_formateada = f"{fecha_publicacion[:4]}-{fecha_publicacion[4:6]}-{fecha_publicacion[6:8]}"

    return fecha_formateada

def obtener_nombre_video(url):
    # Obtener la información del video utilizando yt-dlp en formato JSON
    resultado = subprocess.run(["yt-dlp", "-J", url], capture_output=True, text=True)
    info_video = json.loads(resultado.stdout)
    
    # Obtener el título del video del JSON
    titulo_video = info_video.get("title")

    return titulo_video

def main():
    # Lista de URLs de los videos a descargar
    canales = {
        "Jinn-Topic": ["https://www.youtube.com/watch?v=4Fy6neJmX9s", "https://www.youtube.com/watch?v=XNwzxjB05fE", "https://www.youtube.com/watch?v=SQkFh8XOIcE", "https://www.youtube.com/watch?v=koX7Bua4WZs", "https://www.youtube.com/watch?v=5Ulf9ifvQPQ"],
        # "Canal2": ["URL2_1", "URL2_2", "URL2_3", "URL2_4", "URL2_5"],
        # "Canal3": ["URL3_1", "URL3_2", "URL3_3", "URL3_4", "URL3_5"],
        # "Canal4": ["URL4_1", "URL4_2", "URL4_3", "URL4_4", "URL4_5"],
        # "Canal5": ["URL5_1", "URL5_2", "URL5_3", "URL5_4", "URL5_5"]
    }

    for canal, urls in canales.items():
        for url in urls:
            # Extraccion del nombre del video
            nombre = obtener_nombre_video(url)
            # Descarga del video y extraccion de audio
            descargar_video_y_extraer_audio(url, nombre)
            # Creacion y registro de los datos del video en el archivo registro.csv
            registrar_descarga(canal, url, nombre)
            # Eliminar el video
            os.remove(f"{nombre}.webm")