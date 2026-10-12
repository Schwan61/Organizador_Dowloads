# Organizador Automático de Downloads

Script desenvolvido em Python para monitorar a pasta Downloads do Windows e organizar automaticamente arquivos em subpastas de acordo com suas extensões.

## Funcionalidades

- Monitoramento de novos arquivos na pasta Downloads.
- Organização automática por extensão.
- Criação automática das pastas de destino.
- Prevenção contra sobrescrita de arquivos com nomes iguais.

## Categorias

| Pasta | Extensões |
|---|---|
| Documentos | `.pdf`, `.docx`, `.xlsx` |
| Imagens | `.jpg`, `.jpeg`, `.png`, `.webp` |
| Compactados | `.zip`, `.rar`, `.7z` |
| Instaladores | `.exe`, `.msi` |

## Tecnologias utilizadas

- Python
- Watchdog
- pathlib
- shutil

## Como executar

1. Instale o Python.
2. Clone este repositório ou baixe os arquivos.
3. Instale a dependência:

   `pip install -r requirements.txt`

4. Execute o script:

   `python organizador_downloads.py`

O programa continuará monitorando a pasta Downloads até ser encerrado com `Ctrl + C`.

## Observações

O script monitora novos arquivos enquanto está em execução. Arquivos existentes antes de iniciar o programa não são organizados automaticamente.

## Autor

Projeto pessoal de estudo de Python e automação.
