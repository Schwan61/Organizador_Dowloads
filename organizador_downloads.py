
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import time

# pasta que vai ficar sendo monitorada
DOWNLOADS = Path.home() / "Downloads"

# cada tipo de arquivo vai para uma pasta
CATEGORIAS = {
    "Documentos": {".pdf", ".docx", ".xlsx"},
    "Imagens": {".jpg", ".jpeg", ".png", ".webp"},
    "Compactados": {".zip", ".rar", ".7z"},
    "Instaladores": {".exe", ".msi"},
}


def aguardar_download(arquivo, tentativas=15):
    # espera um pouco para ver se o download terminou
    tamanho_anterior = -1
    estavel = 0

    for _ in range(tentativas):
        try:
            tamanho_atual = arquivo.stat().st_size

            if tamanho_atual == tamanho_anterior:
                estavel += 1
            else:
                estavel = 0

            # se o tamanho não mudar por 3 verificações, continua
            if estavel >= 2:
                return True

            tamanho_anterior = tamanho_atual

        except (FileNotFoundError, PermissionError):
            # pode acontecer se o arquivo ainda estiver sendo baixado
            pass

        time.sleep(1)

    return False


def organizar_arquivo(caminho):
    arquivo = Path(caminho)

    # verifica se o arquivo ainda existe
    if not arquivo.is_file():
        return

    destino_pasta = None

    # olha a extensão e descobre onde guardar
    for pasta, extensoes in CATEGORIAS.items():
        if arquivo.suffix.lower() in extensoes:
            destino_pasta = DOWNLOADS / pasta
            break

    # se não conhecer a extensão, deixa o arquivo quieto
    if destino_pasta is None:
        return

    if not aguardar_download(arquivo):
        print(f"Download ainda não terminou: {arquivo.name}")
        return

    try:
        # cria a pasta caso ela ainda não exista
        destino_pasta.mkdir(parents=True, exist_ok=True)

        destino = destino_pasta / arquivo.name

        # teste: se já existir um arquivo com o mesmo nome,
        # coloca um número no final para não substituir o outro
        contador = 1
        while destino.exists():
            destino = destino_pasta / (
                f"{arquivo.stem} ({contador}){arquivo.suffix}"
            )
            contador += 1

        shutil.move(str(arquivo), str(destino))

        print(f"Arquivo organizado: {arquivo.name} -> {destino_pasta.name}/")

    except (FileNotFoundError, PermissionError, OSError) as erro:
        print(f"Deu erro ao mover {arquivo.name}: {erro}")


class OrganizadorHandler(FileSystemEventHandler):

    # chamado quando aparece um arquivo novo
    def on_created(self, event):
        if not event.is_directory:
            organizar_arquivo(event.src_path)

    # chamado quando um arquivo é movido para a pasta monitorada
    def on_moved(self, event):
        if not event.is_directory:
            organizar_arquivo(event.dest_path)


def main():
    # confere se a pasta Downloads existe
    if not DOWNLOADS.exists():
        print(f"Pasta não encontrada: {DOWNLOADS}")
        return

    observador = Observer()

    # por enquanto, monitora só a pasta principal
    observador.schedule(
        OrganizadorHandler(),
        str(DOWNLOADS),
        recursive=False
    )

    observador.start()

    print(f"Monitorando a pasta: {DOWNLOADS}")
    print("Deixe o programa aberto para ele funcionar.")
    print("Para parar, aperte Ctrl+C.")

    # teste futuro: adicionar um log em arquivo para guardar os movimentos
    # with open("historico.txt", "a", encoding="utf-8") as log:
    #     log.write("Organizador iniciado\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observador.stop()
        print("\nOrganizador encerrado!")

    observador.join()


if __name__ == "__main__":
    main()
