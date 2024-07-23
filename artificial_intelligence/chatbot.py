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
    generation_config=generation_config,
    system_instruction="""Sou assistente do departamento PCP da WEG Energia, irei sempre auxiliar e ajudar da melhor 
        forma possível de acordo com meus conhecimentos;
        Sou uma das IAs que estão dentro do IAron Agent, as outras IAs servem para desenvolvimento de determinados 
        sistemas e eu sirvo para responder perguntas e respostas, irei me basear nos últimos Inputs e Outputs das 
        outras IAs para responder caso exista, se não existir nenhum Input e Output irei me basear no histórico de 
        conversas que eu tive"""
)

class GeminiAI:
    def __init__(self):
        self.chat_session = model.start_chat()
        self.chat_data = []

    def add_history(self, input, output):
        self.chat_data.append(f'input: {input}')
        self.chat_data.append(f'output: {output}')

    def send_message(self, message: str):
        history = "\n".join(self.chat_data)
        message = f"""Inputs e Outputs das outras IAs:
        {history}
        -------------------------------------------------------------------------
        Reponda no idioma no qual está escrito: 
        input: {message}
        output: """
        self.chat_data = []
        response = self.chat_session.send_message(message).text
        return response.strip()
