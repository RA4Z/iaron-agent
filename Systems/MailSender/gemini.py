import google.generativeai as genai
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


def write_mail(prompt: str, data):
    response = model.generate_content([
        f"""Minha tarefa é escrever textos formais para E-mail, esses E-mails sempre serão para pessoas que estão na
        empresa WEG, minhas respostas sempre serão somente um objeto JSON o corpo do E-mail será em HTML e sempre será 
        estilizado de forma atraente e extremamente profissional. NUNCA irei mudar a cor de background do Email
        NÃO POSSO ACRESCENTAR OBSERVAÇÕES NEM NADA DO TIPO EM MEUS OUTPUTS""",
        "\n".join(data),
        f"input: {prompt}",
        "output: "
    ])
    return response.text
