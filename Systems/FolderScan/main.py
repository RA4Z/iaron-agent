import os
from Systems.FolderScan.gemini import scan_files
from Systems.FolderScan.convert_data import create_folder_summary
from Systems.FolderScan.upload_doc import extract_info

def run_system(user_input: str):
    files_text = ''
    pasta = os.path.dirname(user_input.replace('\\', '/'))
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
