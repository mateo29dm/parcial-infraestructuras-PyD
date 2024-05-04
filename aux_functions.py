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
        writer.writerow([f"Nombre del canal: {canal}", 
                        f" Nombre del video:{nombre}", 
                        f" URL: {url}", 
                        f" Fecha de publicacion: {fecha_publicacion}",
                        f" Fecha de descarga: {fecha_descarga}"])


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

def obtener_ultimos_videos(canales_json):
    # Lee el archivo JSON 
    with open(canales_json, 'r') as f:
        data = json.load(f)

    # Obtiene las URLs de los canales
    canales = [canal['url'] for canal in data['canales']]

    resultados = []  # Lista para guardar las URLs de los videos

    # Para cada canal, obtiene las últimas cinco URLs
    for canal in canales:
        # Usa subprocess para ejecutar yt-dlp y obtener los IDs de los últimos 5 videos
        yt_dlp_cmd = f'yt-dlp --flat-playlist --get-id "{canal}" | head -n 5'
        result = subprocess.check_output(yt_dlp_cmd, shell=True)
        
        # Divide la salida en líneas
        ultimos_videos = result.decode('utf-8').split()

        # Convierte los IDs a URLs completas 
        for video_id in ultimos_videos:
            url = f"https://www.youtube.com/watch?v={video_id}"
            resultados.append(url)

    return resultados 
