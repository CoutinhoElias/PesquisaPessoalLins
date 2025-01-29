# Gerar apk Windows
# pip install Pillow
# flet pack .\main.py --icon .\favicon.png --add-data .\assets:assets --hidden-import pymssql pyodbc -n "NovoApp" 

# Usando pyinstaller
# pyinstaller --onefile --add-data ".\assets;assets" --hidden-import pymssql .\main.py

import flet as ft

# Importação de componentes customizados e views
from partials.navigation_drawer import MyNavigationDrawer
from partials.app_bar import MyAppBar
from partials.button import MyButton
from configs.settings import Criptografia
from views.home_view import HomeView
from views.login import Cadastrar, Login
from views.pedido_de_venda_vw import PedidoDeVendaVW
from views.calculo_preco_vw import CalculoPrecoVW
from partials.all_imports import *
# import json
# import os

class App:
    def __init__(self, page: ft.Page):
        """Inicializa a aplicação com a configuração da página e navegação"""
        self.page = page

        # CRIPTOGRAFA
        # 0 - Instancio a classe de criptografar senhas
        self.criptografia = Criptografia()
        # 1 - Chamo a função de criação da chave
        self.criptografia.init_criptografia()

        # Para que eu possa usar essas variáveis em outras classes devo passar a instância self 
        # na chamada das outras classes.
        # Exemplo: view = PedidoNovoViewLocal(self.page, self).get_content()
        # E nas classes, no init assim: def __init__(self, page: ft.Page, app_instance):
        
        self.user_info = None  # Variável para armazenar as informações do usuário
        self.password_api = None # Variável para armazenar as informações do usuário
        self.params_api = None
        self.id_bimer = None # Variável para armazenar as informações do usuário

        # Configurações da página
        self.page.bgcolor = ft.Colors.BLACK
        self.page.title = "Pesquisa Pessoal em Flet v1.01"
        self.page.theme_mode = "dark"  # Define o tema como escuro
        self.page.window.center()  # Centraliza a janela na tela
        
        # Define as dimensões da janela
        # self.page.window_maximized=True
        self.tamanho_tela(899, 1465)

        # Define a animação de transição de páginas
        self.page.theme = ft.Theme(page_transitions={
            'windows': ft.PageTransitionTheme.CUPERTINO
        })

        # Configuração do idioma da aplicação
        self.page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                ft.Locale("pt", "BR"),  # Português, Brasil
                ft.Locale("de", "DE"),  # Alemão, Alemanha
                ft.Locale("fr", "FR"),  # Francês, França
                ft.Locale("es"),        # Espanhol
            ],
            current_locale=ft.Locale("pt", "BR"),  # Define o idioma inicial como Português do Brasil
        )

        self.setup_navigation()  # Configura a navegação
        self.page.update()  # Atualiza a página

    def tamanho_tela(self, height, width):
        self.page.window.width = width
        self.page.window.height = height
        self.page.window.center()
        self.page.update

    def criar_arquivo_cfg(self, dados):
        """Cria o arquivo cfg_sql.json com os dados fornecidos."""
        with open("cfg_sql.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    def verificar_e_criar_cfg(self, page: ft.Page):
        """Verifica se o arquivo cfg_sql.json existe e exibe um modal se necessário."""
        if os.path.exists("cfg_sql.json"):
            print("Arquivo cfg_sql.json já existe.")
            return

        # Função para salvar os dados do modal
        def salvar_cfg(e):
            # Remova a vírgula para que password seja uma string
            password = self.criptografia.criptografar_senha(password_field.content.value)

            # Se você quiser salvar a senha criptografada em um arquivo, faça isso aqui
            # self.criptografia.salvar_senha_criptografada(password)

            dados = {
                "user": user_field.content.value,
                # Aqui você pode usar password diretamente, pois já é a senha criptografada
                "password": password.decode(),  # Se a senha criptografada for em bytes, use decode()
                "host": host_field.content.value,
                "database": database_field.content.value,
            }
            self.criar_arquivo_cfg(dados)
            modal.open = False  # Fecha o modal
            page.update()

        # Função para cancelar e fechar o modal
        def cancelar_cfg(e):
            modal.open = False  # Fecha o modal
            self.page.go("/")
            page.update()

        # Campos do modal
        user_field = ft.Container(ft.TextField(label="Usuário", dense=True), padding=0, margin=0)
        password_field = ft.Container(ft.TextField(label="Senha", password=True, dense=True), padding=0, margin=0)
        host_field = ft.Container(ft.TextField(label="Host", dense=True), padding=0, margin=0)
        database_field = ft.Container(ft.TextField(label="Banco de Dados", dense=True), padding=0, margin=0)

        # Configurando o modal
        modal = ft.AlertDialog(
            title=ft.Text("Configurar Banco de Dados"),
            content=ft.Column(
                [
                    user_field,
                    password_field,
                    host_field,
                    database_field,
                ],
                spacing=5,  # Ajuste o espaçamento conforme necessário
                tight=True,
            ),
            actions_alignment=ft.MainAxisAlignment.END,  # Alinha os botões à direita
            actions=[
                MyButton(text="Salvar", on_click= salvar_cfg, bgcolor=ft.Colors.BLUE_300),
                MyButton(text="Cancelar", on_click= cancelar_cfg),
            ],
            modal=True,
            adaptive=True,
        )

        # Abrindo o modal
        modal.open = True
        page.dialog = modal  # Define o modal na página
        page.update()

    def setup_navigation(self):
        """Configura a navegação da aplicação"""
        def indicador_de_tela(nav_drawer):
            """Atualiza a rota da aplicação com base no item do menu selecionado"""
            menu_selecionado = nav_drawer.selected_index  # Acessa o selected_index diretamente
            match menu_selecionado:
                case 0:
                    self.page.go("/")
                    self.verificar_e_criar_cfg(self.page)
                    # carrega o json de conexão.
                    # print(f"XxXxXxXxXxXxXxXxXxXxXxXxXxXxXx Senha descriptografada: {self.criptografia.get_senha_descriptografada()}")
                case 5:
                    self.page.go("/login")
                    self.verificar_e_criar_cfg(self.page)
                case 6:
                    self.page.go("/login/novo")
                    self.verificar_e_criar_cfg(self.page)
                case 8:
                    self.page.go("/estoque/calculo_preco")
                    self.verificar_e_criar_cfg(self.page)                       
                case 11:
                    self.page.go("/faturamento/importar_xml")
                    self.verificar_e_criar_cfg(self.page)                    
                case _:
                    self.page.go("/")
                    self.verificar_e_criar_cfg(self.page)
            print(f'Selecionei {menu_selecionado}')

        # Define o drawer de navegação e seu comportamento ao mudar a seleção
        self.page.drawer = MyNavigationDrawer(on_change=indicador_de_tela)
        self.page.update()

        def route_change(event):
            """Atualiza a view da aplicação com base na rota"""
            route = event.route
            print(f"Route changed to: {route}")
            self.page.views.clear()  # Limpa as views atuais

            # Define a view e a app bar com base na rota
            match route:
                case "/":
                    view = HomeView().get_content()
                    app_bar_title = f"Pagina Principal"
                    app_bar_color = ft.Colors.GREY_800
                    include_drawer = True
                case "/estoque/calculo_preco":
                    # Se desejar coletar alguma informação da página abaixo deve enviar self como parâmetro.
                    view = CalculoPrecoVW(self.page, self).get_content()
                    app_bar_title = "Calcula custo pelo XML do Fornecedor"
                    app_bar_color = ft.Colors.GREY_800
                    include_drawer = True                    
                case "/faturamento/importar_xml":
                    # Se desejar coletar alguma informação da página abaixo deve enviar self como parâmetro.
                    view = PedidoDeVendaVW(self.page, self).get_content()
                    app_bar_title = "Criar pedido de transferência por XML do Fornecedor"
                    app_bar_color = ft.Colors.GREY_800
                    include_drawer = True
                case "/login":
                    # Se desejar coletar alguma informação da página abaixo deve enviar self como parâmetro.
                    view = Login(self.page, self).get_content()
                    app_bar_title = "Login"
                    app_bar_color = ft.Colors.GREY_800  
                    include_drawer = False
                case "/login/novo":
                    view = Cadastrar(self.page, self).get_content()
                    app_bar_title = "Novo Login"  
                    app_bar_color = ft.Colors.GREY_800 
                    include_drawer = False
                case _:
                    view = HomeView().get_content()
                    app_bar_title = "Pagina Principal"
                    app_bar_color = ft.Colors.GREY_800
                    include_drawer = True

            # Adiciona a nova view com a app bar e o drawer (condicionalmente)
            new_view_content = [
                MyAppBar(app_bar_title, app_bar_color),
                view
            ]
            if include_drawer:
                new_view_content.insert(0, self.page.drawer)

            self.page.views.append(
                ft.View(
                    route,
                    new_view_content
                )
            )
            self.page.update()  # Atualiza a página

        self.page.on_route_change = route_change  # Define o callback para mudanças de rota
        self.page.go("/login")  # Define a rota inicial
        self.page.update

if __name__ == '__main__':
    # Inicializa a aplicação Flet com a classe App como alvo e o diretório de assets
    ft.app(target=App, assets_dir='assets')
