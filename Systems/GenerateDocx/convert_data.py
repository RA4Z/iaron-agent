import markdown
from html2docx import html2docx
import os

def convert_markdown_to_docx(markdown_text, doc_title):
    try:
        # Converter Markdown para HTML
        html = markdown.markdown(markdown_text, extensions=['tables'])

        # Converter HTML para DOCX, definindo o título do documento
        docx_content = html2docx(html, title=doc_title)

        # Converter BytesIO para bytes
        docx_bytes = docx_content.getvalue()

        # Criar o diretório se ele não existir
        diretorio_destino = os.path.join("C:\\", "IAron", "Documents")
        os.makedirs(diretorio_destino, exist_ok=True)

        # Salvar o conteúdo em um arquivo .docx
        caminho_arquivo = os.path.join(diretorio_destino, f"{doc_title}.docx")
        with open(caminho_arquivo, "wb") as f:
            f.write(docx_bytes)

        return f'{caminho_arquivo}'

    except Exception as e:
        return f'Ocorreu o erro {e} ao tentar criar o documento!'
