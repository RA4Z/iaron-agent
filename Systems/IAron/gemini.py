from Systems.IAron.gemini_config import develop_code, develop_input
from Systems.IAron.functions import retornar_codigo, pegar_texto_externo, copiar_pasta, cadastrar_worksheet, send_data
import time

def get_ai_input(user_input: str):
    try:
        return develop_input(user_input)

    except Exception as e:
        print(e)
        return user_input


def run_automation(user_input: str):
    output = develop_code(user_input)
    if output is not None:
        try:
            codigo = retornar_codigo(output)
            documentation = pegar_texto_externo(output)
            file = f"script {time.strftime('%d_%m_%y_%H-%M-%S', time.localtime())}"

            origem = "development/script"
            destino = f"C:\\IAron\\{file}"
            copiar_pasta(origem, destino)

            open(f'C:\\IAron\\{file}\\main.py', 'w', encoding="UTF-8").write(f"{codigo}")
            open(f'C:\\IAron\\{file}\\README.md', 'w', encoding="UTF-8").write(f"{documentation}")
            cadastrar_worksheet(output, destino)
            send_data(user_input, output, codigo, documentation)
            return destino

        except Exception as e:
            print(e)
            return ""

    else:
        return ""


if __name__ == '__main__':
    run_automation('Teste')
    print('Código Criado')
