import PyPDF2
from docx import Document

def extract_txt(filename: str):
    texto = ''
    try:
        with open(filename, 'r', encoding='utf-8') as arquivo:
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

def extract_info(file):  # Corrigido: recebe FilePickerFile
    if file.name.endswith(".docx"):  # Acessa o nome usando file.name
        return extract_docx(file.path)  # Passa o caminho do arquivo para extract_docx

    if file.name.endswith(".pdf"):  # Acessa o nome usando file.name
        return extract_pdf(file.path)  # Passa o caminho do arquivo para extract_pdf

    if file.name.endswith(".txt"):  # Acessa o nome usando file.name
        return extract_txt(file.path)  # Passa o caminho do arquivo para extract_txt


if __name__ == '__main__':
    pass
