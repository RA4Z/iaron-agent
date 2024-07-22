import PyPDF2
import json
from docx import Document
from excel import ExcelHandler

def extract_excel(filename: str):
    excel = ExcelHandler(filename)
    excel.load_workbook()
    excel.select_sheet(excel.workbook.active.title)
    cols = excel.count_columns(1)

    # Encontrar a coluna com mais linhas não vazias
    max_rows = 0
    for c in range(1, cols + 1):
        rows_in_column = 0
        for i in range(1, excel.count_rows(c) + 1):
            if excel.get_cell(i, c) is not None:
                rows_in_column += 1
        max_rows = max(max_rows, rows_in_column)

    # Criar a matriz
    table_data = []
    for i in range(1, max_rows + 1):
        active_row = []
        for c in range(1, cols + 1):
            active_row.append(excel.get_cell(i, c))
        table_data.append(active_row)

    matriz = ''
    # Imprimir a matriz formatada
    for row in table_data:
        for cell in row:
            matriz = matriz + f"{cell}\t"
        matriz = matriz + '\n'
    return matriz

def extract_txt(filename: str):
    texto = ''
    try:
        with open(filename, 'r') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                texto = texto + linha

    except FileNotFoundError:
        print("Arquivo não encontrado.")

    return texto

def extract_docx(filename: str):
    try:
        doc = Document(filename)
        texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        texto = ''
        print(e)

    return texto

def extract_pdf(filename: str):
    all_text = ""
    try:
        pdf_file_obj = open(filename, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        for page_num in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            text = page_obj.extract_text()
            all_text += text

        pdf_file_obj.close()
    except Exception as e:
        print(e)

    return all_text

def extract_json(filename: str):
    return json.load(open(filename, 'r', encoding='utf-8'))

def extract_info(file):  # Corrigido: recebe FilePickerFile
    if file.endswith(".docx"):  # Acessa o nome usando file.name
        return extract_docx(file)  # Passa o caminho do arquivo para extract_docx

    if file.endswith(".pdf"):  # Acessa o nome usando file.name
        return extract_pdf(file)  # Passa o caminho do arquivo para extract_pdf

    if file.endswith((".txt", ".py", ".md", ".log")):  # Acessa o nome usando file.name
        return extract_txt(file)  # Passa o caminho do arquivo para extract_txt

    if file.endswith((".xlsx", "xlsm")):  # Acessa o nome usando file.name
        return extract_excel(file)  # Passa o caminho do arquivo para extract_excel

    if file.endswith(".json"):  # Acessa o nome usando file.name
        return extract_json(file)  # Passa o caminho do arquivo para extract_json

    return ''
