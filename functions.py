import subprocess
import requests
import getpass

def select_iaron_developer(user_input: str):
    from Systems.IAron.gemini import run_automation
    response = run_automation(user_input)
    if response != '':
        subprocess.run(['python', f'{response}/main.py'], check=True)
        return f'Arquivo criado com sucesso em {response}'


def select_iaron_run_code(user_input: str):
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
