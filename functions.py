from upload_doc import extract_docx
from artificial_intelligence.chatbot import GeminiAI
import win32com.client
import pythoncom
import subprocess

ia = GeminiAI()

def select_iaron_developer(user_input: str):
    from Systems.IAron.gemini import run_automation, get_ai_input
    tuned_input = get_ai_input(user_input)
    response = run_automation(tuned_input)
    if response != '':
        ia.add_history(user_input, response)
        subprocess.run(['python', f'{response}/main.py'], check=True)
        return f'Arquivo criado com sucesso em {response}'


def select_iaron_dev_code(user_input: str):
    from Systems.IAron.gemini import run_automation
    response = run_automation(f""" Observação: Importar funções os e sys no começo do código\n {user_input}""")
    if response != '':
        ia.add_history(user_input, response)
        subprocess.run(['python', f'{response}/main.py'], check=True)
        return f'Arquivo criado com sucesso em {response}'

def select_chatbot_ppc(user_input: str):
    try:
        response = ia.send_message(user_input)
        return response
    except Exception as e:
        return f'Ocorreu o erro {str(e)} ao tentar executar a função select_chatbot_ppc!'

def select_send_email(user_input: str):
    from Systems.MailSender.main import run_system
    response = run_system(user_input)
    ia.add_history(user_input, response)
    return response

def select_folder_scan(user_input: str):
    from Systems.FolderScan.main import run_system
    response = run_system(user_input)
    try:
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Documents.Open(response)
        word.Visible = True

    except Exception as e:
        print(e)

    ia.add_history(user_input, extract_docx(response))
    return f'Documento criado com sucesso em {response}'

def select_create_docx(user_input: str):
    from Systems.GenerateDocx.main import run_system
    response = run_system(user_input)
    try:
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Documents.Open(response)
        word.Visible = True

    except Exception as e:
        print(e)

    ia.add_history(user_input, extract_docx(response))
    return f'Documento criado com sucesso em {response}'

def select_create_docx_and_send_email(user_input):
    import Systems.GenerateDocx.main
    file_path = Systems.GenerateDocx.main.run_system(f'{user_input} NÃO CITE O NOME DE QUEM RECEBERÁ O EMAIL, APENAS '
                                                     f'GERE O TEXTO PARA O DOCUMENTO').replace('\\', '/')
    try:
        user_input = f"{user_input}\n Dados do anexo {file_path}:\n {extract_docx(file_path)}"

    except Exception as e:
        print(e)

    ia.add_history(user_input, extract_docx(file_path))
    return select_send_email(f'{user_input} FAÇA UM BREVE RESUMO DESSE TEXTO PARA SER UTILIZADO NO CORPO DO EMAIL, '
                             f'QUERO QUE SEJA ALGO QUE FAÇA COM QUE A PESSOA QUE ESTÁ RECEBENDO O EMAIL SINTA VONTADE '
                             f'DE ABRIR O DOCUMENTO EM ANEXO. PARA O CORPO DO EMAIL FAÇA UM CÓDIGO HTML BONITO, '
                             f'ATRAENTE E CHAMATIVO')

def select_excel_macro(user_input):
    from Systems.ExcelMacros.main import run_system
    return run_system(user_input)
