import tkinter as tk
from Systems.IAron.gemini_config import develop_input
from tkinter import filedialog
from Systems.IAron.extract_data import extrair_info

def selecionar_arquivo():
    # Cria a janela raiz, mas não a exibe
    root = tk.Tk()
    root.withdraw()

    # Define os tipos de arquivo permitidos
    filetypes = (
        ('Documentos Word', '*.docx'),
        ('Documentos PDF', '*.pdf'),
        ('Todos os arquivos', '*.*')
    )

    # Abre a janela de diálogo para seleção de arquivo
    arquivo = filedialog.askopenfilename(
        title='Selecione um arquivo',
        filetypes=filetypes
    )

    # Destroi a janela raiz após o uso
    root.destroy()

    # Verifica se o usuário selecionou um arquivo
    if arquivo:
        data = extrair_info(arquivo)
        result = develop_input(data)
        return result
    else:
        return None


if __name__ == '__main__':
    output = selecionar_arquivo()
    if output:
        print(output)
