import json
from Systems.ExcelMacros.gemini import run_excel_macro
from Systems.ExcelMacros.excel import automate

def run_system(user_input: str):
    data = []
    inputs = json.load(open('database/macro_calls.json', 'r', encoding='utf-8'))
    for value in inputs:
        data.append(f"input: {value['input']}")
        data.append(f"output: {value['output']}")

    response = (run_excel_macro(f'Crie o output necessário para execução de macros baseando-se no input a seguir:'
                                f'{user_input}.\n SEMPRE ESCREVA USANDO INFORMAÇÕES DO CONTEÚDO DO INPUT.'
                                f'não me dê sugestões, apenas o resultado', data)
                .replace('`', '').replace('json', '').strip().replace('\\', '\\\\'))
    try:
        response = json.loads(response)

    except json.JSONDecodeError as e:
        print(f"Erro ao analisar JSON: {e}")
        print(f"String JSON inválida: {response}")

    print(response['worksheet'])
    automate(response['worksheet'], response['script'])

    return f"Macro {response['worksheet']} executada com sucesso!"


if __name__ == '__main__':
    run_system('Atualiza o CRP para mim')
