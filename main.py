import argparse
import timeit
from yt_audio_downloader_mt import main as multithreading_main
from yt_audio_downloader_sq import main as sequential_main
from yt_audio_downloader_mp import main as multiprocessing_main
from aux_functions import obtener_ultimos_videos

# Lista para almacenar los enlaces de los últimos 5 vídeos de cada canal
urls = []

def main():

    start = timeit.default_timer()
    canales = "canales.json"

    urls = obtener_ultimos_videos(canales)

    parser = argparse.ArgumentParser(description="Descargar videos de YouTube y extraer su audio utilizando múltiples hilos.")
    parser.add_argument("--modo", choices=["sq", "mt", "mp"], default="sq", help="Modo de ejecucion, sq = sequencial, mt= multithreading, mp = multiprocessing. (por defecto sequencial)")
    parser.add_argument("--workers", type=int, default=4, help="Número de workers a utilizar (por defecto: 4, solo para multithreading y multiprocessing)")
    args = parser.parse_args()

    end = timeit.default_timer()

    tiempo_inicializacion = end - start

    if args.modo == "mt":
        multithreading_main(urls, args.workers, tiempo_inicializacion)
    elif args.modo == "sq":
        sequential_main(urls, tiempo_inicializacion)
    elif args.modo == "mp":
        multiprocessing_main(urls, args.workers, tiempo_inicializacion)

if __name__ == "__main__":
    main()