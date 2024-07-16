import json
import functions
from artificial_intelligence.gemini import decidir_tarefa

def run_system(user_input: str):
    data = []
    inputs = json.load(open('database/select_function.json', 'r', encoding='utf-8'))
    for value in inputs:
        data.append(f"input: {value['input']}")
        data.append(f"output: {value['output']}")

    return decidir_tarefa(f'Cite o nome da função correta baseada no input do usuário a seguir: {user_input}', data)


def choose(func: str, user_input: str):
    try:
        call_function = getattr(functions, func.strip())
        return call_function(user_input)
    except Exception as e:
        return f'Ocorreu o erro: {str(e)} ao tentar invocar a função {func}!'


if __name__ == '__main__':
    user_input = """"""
    response = run_system(user_input)
    print(f'Executando a função {response.strip()}...')
    print(choose(response, user_input))
