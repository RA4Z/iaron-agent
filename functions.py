from upload_doc import extract_docx
import win32com.client
import pythoncom
import subprocess
import requests
import getpass

def select_iaron_developer(user_input: str):
    from Systems.IAron.gemini import run_automation, get_ai_input
    tuned_input = get_ai_input(user_input)
    response = run_automation(tuned_input)
    if response != '':
        subprocess.run(['python', f'{response}/main.py'], check=True)
        return f'Arquivo criado com sucesso em {response}'


def select_iaron_dev_code(user_input: str):
    from Systems.IAron.gemini import run_automation
    response = run_automation(f""" Observação: Importar funções os e sys no começo do código\n {user_input}""")
    if response != '':
        subprocess.run(['python', f'{response}/main.py'], check=True)
        return f'Arquivo criado com sucesso em {response}'

def select_chatbot_ppc(user_input: str):
    try:
        url = 'http://10.1.43.63:5000/gemini'
        data = {
            'message': user_input,
            'username': getpass.getuser()
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            return response.text
        else:
            return f'Ocorreu o erro: {response.status_code}!'
    except Exception as e:
        return f'Ocorreu o erro {e}!'

def select_send_email(user_input: str):
    from Systems.MailSender.main import run_system
    return run_system(user_input)

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

    return f'Documento criado com sucesso em {response}'

def select_create_docx_and_send_email(user_input):
    import Systems.GenerateDocx.main
    file_path = Systems.GenerateDocx.main.run_system(f'{user_input} NÃO CITE O NOME DE QUEM RECEBERÁ O EMAIL, APENAS '
                                                     f'GERE O TEXTO PARA O DOCUMENTO').replace('\\', '/')
    try:
        user_input = f"{user_input}\n Dados do anexo {file_path}:\n {extract_docx(file_path)}"

    except Exception as e:
        print(e)

    return select_send_email(f'{user_input} FAÇA UM BREVE RESUMO DESSE TEXTO PARA SER UTILIZADO NO CORPO DO EMAIL, '
                             f'QUERO QUE SEJA ALGO QUE FAÇA COM QUE A PESSOA QUE ESTÁ RECEBENDO O EMAIL SINTA VONTADE '
                             f'DE ABRIR O DOCUMENTO EM ANEXO. PARA O CORPO DO EMAIL FAÇA UM CÓDIGO HTML BONITO, '
                             f'ATRAENTE E CHAMATIVO')
