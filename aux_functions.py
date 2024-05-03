import datetime
import csv
import subprocess
import json

def registrar_descarga(url, nombre):
    fecha_descarga = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_publicacion = obtener_fecha_publicacion(url)
    canal = obtener_nombre_canal(url)
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

def obtener_nombre_canal(url):
    # Obtener la información del video utilizando yt-dlp en formato JSON
    resultado = subprocess.run(["yt-dlp", "-J", url], capture_output=True, text=True)
    info_video = json.loads(resultado.stdout)
    
    # Obtener el nombre del canal del JSON
    nombre_canal = info_video.get("channel")

    return nombre_canal