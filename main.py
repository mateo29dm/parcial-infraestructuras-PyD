import argparse
from yt_audio_downloader_mt import main as multithreading_main
from yt_audio_downloader_sq import main as sequential_main
from yt_audio_downloader_mp import main as multiprocessing_main


def main():
    parser = argparse.ArgumentParser(description="Descargar videos de YouTube y extraer su audio utilizando múltiples hilos.")
    parser.add_argument("--modo", choices=["sq", "mt", "mp"], default="sq", help="Modo de ejecucion, sq = sequencial, mt= multithreading, mp = multiprocessing. (por defecto sequencial)")
    parser.add_argument("--workers", type=int, default=4, help="Número de workers a utilizar (por defecto: 4, solo para multithreading y multiprocessing)")
    args = parser.parse_args()

    if args.modo == "mt":
        multithreading_main(args.workers)
    elif args.modo == "sq":
        sequential_main()
    elif args.modo == "mp":
        multiprocessing_main(args.workers)

if __name__ == "__main__":
    main()