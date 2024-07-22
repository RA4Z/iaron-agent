import json
from Systems.MailSender.gemini import write_mail
from Systems.MailSender.functions import Outlook


def run_system(user_input):
    data = []
    inputs = json.load(open('database/mail_templates.json', 'r', encoding='utf-8'))
    for value in inputs:
        data.append(f"input: {value['input']}")
        data.append(f"output: {value['output']}")

    response = (write_mail(f'Escreva um E-mail formal baseado no texto a seguir: {user_input}. SEMPRE ESCREVA UM'
                           f'EMAIL COMPLETO USANDO COMO BASE O ASSUNTO.'
                           f'Escreva esse email '
                           f'no idioma que foi escrito a mensagem, não me dê sugestões, apenas o resultado', data)
                .replace('`', '').replace('json', '').strip())
    try:
        response = json.loads(response)

    except json.JSONDecodeError as e:
        print(f"Erro ao analisar JSON: {e}")
        print(f"String JSON inválida: {response}")

    mail = Outlook()
    mail.send_email(subject=response['subject'], to=response['to'], cc=response['cc'], bcc=response['bcc'],
                    body=response['body'], attachments=response['attachments'])

    return f"Email com o título {response['subject']} criado com sucesso!"


if __name__ == '__main__':
    user_input = ''
    run_system(user_input)
