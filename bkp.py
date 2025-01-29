# import flet as ft

# class MyNavigationDrawer(ft.NavigationDrawer):

#     def __init__(self, on_change):
#         super().__init__()

#         self.selected_index = 0
#         self.on_change = on_change

#         # ExpansionTile com submenus
#         self.expansion_tile = ft.ExpansionTile(
#             title=ft.Text("Menu principal"),
#             subtitle=ft.Text("Expanda para ver opções"),
#             controls=[
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.HOME),
#                     title=ft.Text("Página Inicial"),
#                     on_click=lambda _: self._on_tile_click(0),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.LOGIN),
#                     title=ft.Text("Login"),
#                     on_click=lambda _: self._on_tile_click(5),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.APP_REGISTRATION),
#                     title=ft.Text("Novo Cadastro"),
#                     on_click=lambda _: self._on_tile_click(6),
#                 ),
#             ],
#         )

#         # ExpansionTile com submenus
#         self.expansion_tile = ft.ExpansionTile(
#             title=ft.Text("Menu secundário"),
#             subtitle=ft.Text("Expanda para ver opções"),
#             controls=[
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.HOME),
#                     title=ft.Text("Página Inicial"),
#                     on_click=lambda _: self._on_tile_click(0),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.LOGIN),
#                     title=ft.Text("Login"),
#                     on_click=lambda _: self._on_tile_click(5),
#                 ),
#                 ft.ListTile(
#                     leading=ft.Icon(ft.icons.APP_REGISTRATION),
#                     title=ft.Text("Novo Cadastro"),
#                     on_click=lambda _: self._on_tile_click(6),
#                 ),
#             ],
#         )

#         # Adiciona o ExpansionTile e outros controles ao drawer
#         self.controls = [
#             ft.Container(height=12),
#             ft.Image(
#                 src="images\\logo_sv.png",
#                 width=100,
#                 height=200,
#                 fit=ft.ImageFit.CONTAIN,
#                 repeat=ft.ImageRepeat.NO_REPEAT,
#                 border_radius=ft.border_radius.all(10),
#             ),
#             self.expansion_tile,
#             ft.Divider(thickness=2),
#         ]

#         self.bgcolor = ft.colors.BACKGROUND

#     def _on_tile_click(self, index):
#         """
#         Atualiza o índice selecionado e chama o callback `on_change`.
#         """
#         self.selected_index = index  # Atualiza o índice selecionado
#         if self.on_change:
#             self.on_change(self)  # Passa a própria instância da classe para o callback

import flet as ft

class MyNavigationDrawer(ft.NavigationDrawer):
    def __init__(self, on_change):
        super().__init__()

        self.selected_index = 0
        self.on_change = on_change
        self.controls = []

        # Configuração inicial de grupos e itens
        self.groups = [
            {
                "title": "Menu Principal",
                "subtitle": "Expanda para ver opções",
                "items": [
                    {"label": "Home", "icon": ft.icons.HOME, "index": 0},
                    {"label": "Login", "icon": ft.icons.LOGIN, "index": 5},
                    {"label": "Novo Login", "icon": ft.icons.PERSON_ADD, "index": 6},
                ],
            },
            {
                "title": "Outras Opções",
                "subtitle": "Mais funcionalidades",
                "items": [
                    {"label": "Configurações", "icon": ft.icons.SETTINGS, "index": 7},
                    {"label": "Ajuda", "icon": ft.icons.HELP, "index": 8},
                ],
            },
        ]

        self.build_drawer()

    def build_drawer(self):
        """Cria os ExpansionTiles dinamicamente com base nos grupos."""
        self.controls.clear()  # Limpa os controles atuais
        self.controls.append(ft.Container(height=12))  # Espaçamento inicial

        for group in self.groups:
            expansion_tile = ft.ExpansionTile(
                title=ft.Text(group["title"]),
                subtitle=ft.Text(group["subtitle"]),
                maintain_state=True,
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(item["icon"]),
                        title=ft.Text(item["label"]),
                        on_click=lambda e, idx=item["index"]: self._on_tile_click(idx),
                    )
                    for item in group["items"]
                ],
            )
            self.controls.append(expansion_tile)

    def _on_tile_click(self, index):
        """Atualiza o índice selecionado e chama o callback `on_change`."""
        self.selected_index = index
        if self.on_change:
            self.on_change(self)
