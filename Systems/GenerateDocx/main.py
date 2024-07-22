import json
import re
from Systems.GenerateDocx.gemini import write_docx
from Systems.GenerateDocx.convert_data import convert_markdown_to_docx


def run_system(user_input: str):
    data = []
    titulo = ''
    inputs = json.load(open('database/docx_templates.json', 'r', encoding='utf-8'))
    for value in inputs:
        data.append(f"input: {value['input']}")
        data.append(f"output: {value['output']}")

    response = (write_docx(f'Escreva um Documento baseado no texto a seguir: {user_input}. SEMPRE ESCREVA UM'
                           f'DOCUMENTO COMPLETO USANDO COMO BASE O ASSUNTO. Escreva  '
                           f'no idioma que foi escrito a mensagem, não me dê sugestões, apenas o resultado. Entregue a '
                           f'resposta exatamente no mesmo padrão que está no histórico de conversas', data))

    try:
        inicio = response.find("{") + 1
        fim = response.find("}")
        titulo = str(response[inicio:fim])
        response = response.replace("{" + titulo + "}", '')
        titulo = re.sub(r'[^a-zA-Z0-9\s]', '', titulo).replace(':', '')

    except json.JSONDecodeError as e:
        print(f"Erro ao buscar titulo: {e}")

    if titulo == '':
        titulo = 'Título não detectado'

    return convert_markdown_to_docx(response, titulo)
