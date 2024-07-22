import os
import re
from Systems.FolderScan.gemini import scan_files
from Systems.FolderScan.convert_data import create_folder_summary
from Systems.FolderScan.upload_doc import extract_info

def run_system(user_input: str):
    files_text = ''
    padrao_windows = r"[A-Z]:\\(?:[^\\/:*?\"<>|]+\\)*[^\\/:*?\"<>|]+"
    padrao_url = (r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9("
                  r")@:%_\+.~#?&//=]*)")

    resultado_windows = re.search(padrao_windows, user_input)
    resultado_url = re.search(padrao_url, user_input)

    if resultado_windows:
        pasta = resultado_windows.group(0)
    elif resultado_url:
        pasta = resultado_url.group(0)
    else:
        pasta = None

    pasta = pasta.replace('https://intranet.weg.net', '\\\\intranet.weg.net@SSL\\DavWWWRoot')
    pasta = os.path.dirname(pasta.replace('\\', '/').replace('%20', ' '))
    print(pasta)
    if os.path.exists(pasta):
        for nome_arquivo in os.listdir(pasta):
            caminho_completo = os.path.join(pasta, nome_arquivo)
            info = extract_info(caminho_completo)
            if info != '':
                files_text = f'{files_text}\n\nConteúdo do arquivo {nome_arquivo}:\n{info}'

        response = (scan_files(f'Faça uma análise profunda em cada um dos arquivos em anexo: {files_text}'))
        return create_folder_summary(response)
    else:
        return 'Pasta não encontrada'
