from docx import Document
import PyPDF2

def extrair_procedimento(filename: str):
    try:
        doc = Document(filename)
        texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        texto = ''
        print(e)

    return texto


def extrair_pdf(filename: str):
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


def extrair_info(filename: str):
    if filename.endswith(".docx"):
        return extrair_procedimento(filename)

    if filename.endswith(".pdf"):
        return extrair_pdf(filename)
