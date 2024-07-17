import flet as ft
import getpass
import subprocess
from ai_caller import run_system, choose
from upload_doc import extract_info
from languages.translation import Language

lang = Language()

def change_language(language):
    global lang
    with open('languages/selected.txt', 'w', encoding='utf-8') as file:
        file.write(language)
    lang = Language()

class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


def get_avatar_color(user_name: str):
    colors_lookup = [
        ft.colors.AMBER,
        ft.colors.BLUE,
        ft.colors.BROWN,
        ft.colors.CYAN,
        ft.colors.GREEN,
        ft.colors.INDIGO,
        ft.colors.LIME,
        ft.colors.ORANGE,
        ft.colors.PINK,
        ft.colors.PURPLE,
        ft.colors.RED,
        ft.colors.TEAL,
        ft.colors.YELLOW,
    ]
    return colors_lookup[hash(user_name) % len(colors_lookup)]


def get_initials(user_name: str):
    if user_name:
        return user_name[:1].capitalize()
    else:
        return "Desconhecido"  # or any default value you prefer


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.wrap = True
        # Define o conteúdo do CircleAvatar com base no usuário
        avatar_content = (
            ft.Image(
                src="assets/chatbot.png",
                fit=ft.ImageFit.COVER
            )
            if message.user_name == "IAron Agent"
            else ft.Text(get_initials(message.user_name))
        )

        # Define a cor de fundo do CircleAvatar com base no usuário
        avatar_bgcolor = None if message.user_name == "IAron Agent" else get_avatar_color(message.user_name)

        self.controls = [
            ft.CircleAvatar(
                content=avatar_content,
                color=ft.colors.WHITE,
                bgcolor=avatar_bgcolor,
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight=ft.FontWeight.BOLD),
                    ft.Markdown(
                        message.text,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    )
                ],
                tight=True,
                spacing=5,
            )
        ]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "IAron Agent AI"
    arquivos_carregados = []

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = lang.search('blank')
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} {lang.search('joined')}",
                    message_type="login_message",
                )
            )
            page.update()

    def send_message_click(e):
        file_prompt = ''
        if arquivos_carregados:
            for file in arquivos_carregados:
                file_prompt = file_prompt + extract_info(file)

        actual_message = new_message.value
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    f'{new_message.value.strip()}',
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

            response = run_system(actual_message)
            if "select_chatbot_ppc" not in response:
                page.pubsub.send_all(
                    Message(
                        "IAron Agent",
                        f'{lang.search("running")} {response.strip()}...',
                        message_type="chat_message",
                    )
                )
                page.update()

            page.pubsub.send_all(
                Message(
                    "IAron Agent",
                    f'{choose(response, f"{actual_message} {file_prompt}").strip()}',
                    message_type="chat_message",
                )
            )
            page.update()

    def on_message(message: Message):
        global m
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    join_user_name = ft.TextField(
        label=lang.search('insert_name'),
        value=getpass.getuser().capitalize(),
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text(lang.search('welcome')),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text=lang.search('join'), on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text=lang.search('write_prompt'),
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    def upload_arquivos(e: ft.FilePickerResultEvent):
        nonlocal arquivos_carregados
        if e.files is not None:
            arquivos_permitidos = [arquivo for arquivo in e.files
                                   if arquivo.name.lower().endswith(('.docx', '.pdf', '.txt', '.xlsx', '.xlsm'))]

            if arquivos_permitidos:
                arquivos_carregados.extend(arquivos_permitidos)
                atualizar_lista_arquivos()

    def atualizar_lista_arquivos():
        row_arquivos.controls.clear()
        for i, arquivo in enumerate(arquivos_carregados):
            botao_arquivo = ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Text(arquivo.name),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, indice=i: remover_arquivo(indice),
                            icon_color=ft.colors.RED  # Define a cor do ícone
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # Alinha o texto e o ícone
                ),
                on_click=lambda e, indice=i: abrir_arquivo(indice)
            )
            row_arquivos.controls.append(botao_arquivo)
        page.update()

    def abrir_arquivo(indice):
        caminho_completo = arquivos_carregados[indice].path
        try:
            subprocess.run(["start", caminho_completo], shell=True)  # Para Windows

        except FileNotFoundError:
            print(f"Erro ao abrir o arquivo: {caminho_completo}")

    def remover_arquivo(indice):
        del arquivos_carregados[indice]
        atualizar_lista_arquivos()

    def dropdown_changed(e):
        change_language(lang_selector.value)
        page.dialog.actions[0].text = lang.search('join')
        page.dialog.title.value = lang.search('welcome')
        join_user_name.label = lang.search('insert_name')
        new_message.hint_text = lang.search('write_prompt')
        upload_component.tooltip = lang.search('file_upload')
        page.controls[2].controls[2].tooltip = lang.search('send_prompt')
        page.controls[3].content.controls[1].value = lang.search('footer_text')
        lang_selector.hint_text = lang.search('select_language')
        page.update()

    lang_selector = ft.Dropdown(
        on_change=dropdown_changed,
        hint_text=lang.search('select_language'),
        options=[
            ft.dropdown.Option("EN"),
            ft.dropdown.Option("PT"),
            ft.dropdown.Option("ES"),
            ft.dropdown.Option("FR"),
            ft.dropdown.Option("DE"),
        ],
        width=200,
    )

    row_arquivos = ft.Row(wrap=True)

    upload_component = ft.IconButton(
                    icon=ft.icons.UPLOAD_FILE,
                    tooltip=lang.search('file_upload'),
                    on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        row_arquivos,
        ft.Row(
            [
                upload_component,
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip=lang.search('send_prompt'),
                    on_click=send_message_click,
                ),
            ]
        ),
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Image(src="assets/logo.png", width=100, height=50),
                    ft.Text(
                        value=lang.search('footer_text'),
                        size=12,
                        weight=ft.FontWeight.NORMAL,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    lang_selector
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
        )
    )
    file_picker = ft.FilePicker(on_result=upload_arquivos)
    page.overlay.append(file_picker)
    page.update()


if __name__ == '__main__':
    ft.app(target=main)
