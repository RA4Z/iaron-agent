import json
from gemini import write_mail
from functions import Outlook

def run_system(user_input):
    data = []
    inputs = json.load(open('mail_templates.json', 'r', encoding='utf-8'))
    for value in inputs:
        data.append(f"input: {value['input']}")
        data.append(f"output: {value['output']}")
    return write_mail(f'Escreva um E-mail formal baseado no texto a seguir: {user_input}', data)


if __name__ == '__main__':
    user_input = 'Resumo sobre Inflação, enviar de forma oculta para global@email.com'
    response = run_system(user_input).replace('`', '').replace('json', '').strip()

    try:
        response = json.loads(response)
        print(response['to'])
        print(response['cc'])
        print(response['bcc'])
        print(response['subject'])
        print(response['body'])

    except json.JSONDecodeError as e:
        print(f"Erro ao analisar JSON: {e}")
        print(f"String JSON inválida: {response}")

    mail = Outlook()
    mail.send_email(subject=response['subject'], to=response['to'], cc=response['cc'], bcc=response['bcc'],
                    body=response['body'])
