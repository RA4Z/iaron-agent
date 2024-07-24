import google.generativeai as genai
import os
from languages.translation import Language

lang = Language()

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 50000,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config
)


def run_excel_macro(prompt: str, data):
    response = model.generate_content([
        f"""Minha tarefa é retornar o caminho e nome das planilhas com macro e também o nome da macro a ser executada
        nas mesmas, irei utilizar as informações que recebi de input para criar essa resposta
        NÃO POSSO ACRESCENTAR OBSERVAÇÕES NEM NADA DO TIPO EM MEUS OUTPUTS, por padrão minhas respostas serão em 
        {lang.search('Language')}""",
        "\n".join(data),
        f"input: {prompt}",
        "output: "
    ])
    return response.text