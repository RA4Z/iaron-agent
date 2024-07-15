import google.generativeai as genai
from Systems.IAron.gemini_data import data, data_inputs
from Systems.IAron.language_translation import Language
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
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


def develop_input(prompt: str):
    lang = Language()
    response = model.generate_content([
        f"""Minhas respostas sempre serão no idioma {lang.search('idioma')}. 
    Irei converter meu input em uma forma legível e acrescentarei detalhes cruciais sobre o fluxo do procedimento, 
    facilitando o passo a passo para desenvolvimento futuro, irei citar com detalhes onde o código deve clicar ou o que 
    deve fazer em cada etapa, focando no melhor desempenho e na melhor legibilidade.
    Caso no procedimento não esteja descrito com exatidão como fazer algo, somente citando brevemente, utilizarei do 
    conhecimento que possuo no meu histórico de conversas.
    Meu output SEMPRE será em formato de TEXTO PURO, JAMAIS irei utilizar algum texto Markdown como output""",
        "\n".join(data_inputs),
        f"input: {prompt}",
        "output: "
    ])
    return response.text


def develop_code(prompt: str):
    lang = Language()
    response = model.generate_content([
        f"""Sempre irei criar o código em Python e entregar uma documentação sobre o código em {lang.search('idioma')}. 
  ao terminar de escrever o código eu irei escrever "----fimpython----",
  Todo código que eu criar a primeira linha será: # Default model for SAP automations, developed by Robert Aron 
  Zimmermann, using Google AI Studio tuned prompt model;
  Após escrever todo o código, eu irei escrever uma documentação detalhada sobre o mesmo, nessa documentação sempre 
  citarei o nome quem solicitou e também o nome do criador. Nessa documentação explique as funções e também todo o fluxo 
  do sistema na ordem em que ocorre, irei explicar de uma forma profissional e formal, de uma maneira que seja entendido 
  por todos os usuários, até mesmo por quem não tem nenhum conhecimento em programação""",
        "\n".join(data),
        f"input: {prompt}",
        "output: "
    ])
    return response.text
