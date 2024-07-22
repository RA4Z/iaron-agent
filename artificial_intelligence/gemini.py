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


def decidir_tarefa(prompt: str, data):
    response = model.generate_content([
        f"""Minha tarefa é sempre dizer qual a melhor função a ser realizada de acordo com o input do usuário;
        Quando não tiver certeza de qual a melhor função, ou o input do usuário for inválido, vago ou em branco, 
        Minha resposta SEMPRE SERÁ SOMENTE O NOME DA FUNÇÃO INDEPENDENTE DO QUE ACONTECER
        então minha resposta será "select_chatbot_ppc" """,
        "\n".join(data),
        f"input: {prompt}",
        "output: "
    ])
    return response.text
