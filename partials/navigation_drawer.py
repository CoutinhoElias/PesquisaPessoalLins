import flet as ft

class MyNavigationDrawer(ft.NavigationDrawer):
    def __init__(self, on_change):
        super().__init__()
        self.expansion_states = []  # Lista para controlar o estado dos ExpansionTiles
        self.selected_index = 0
        self.on_change = on_change
        self.controls = []

        # Configuração inicial de grupos e itens
        self.groups = [
            {
                "title": "Menu Principal",
                "subtitle": "Expanda para ver opções",
                "collapsed_text_color": ft.Colors.GREEN,
                "items": [
                    {"label": "Home", "icon": ft.icons.HOME, "index": 0},
                    {"label": "Login", "icon": ft.icons.LOGIN, "index": 5},
                    {"label": "Novo Login", "icon": ft.icons.PERSON_ADD, "index": 6},
                ],
            },
            {
                "title": "Estoque",
                "subtitle": "Controles de estoque",
                "collapsed_text_color": ft.Colors.RED,
                "items": [
                    # {"label": "Home", "icon": ft.icons.FACT_CHECK, "index": 7},
                    # {"label": "Home", "icon": ft.icons.INVENTORY, "index": 8},
                    # {"label": "Home", "icon": ft.icons.PAID, "index": 9},
                    # {"label": "Home", "icon": ft.icons.MONETIZATION_ON, "index": 10},
                    {"label": "Ajuste de custo por XML", "icon": ft.icons.ATTACH_MONEY, "index": 8},
                ],
            },            
            {
                "title": "Faturamento",
                "subtitle": "Notas emitidas",
                "collapsed_text_color": ft.Colors.BLUE,
                "items": [
                    # {"label": "Home", "icon": ft.icons.FACT_CHECK, "index": 7},
                    # {"label": "Home", "icon": ft.icons.INVENTORY, "index": 8},
                    # {"label": "Home", "icon": ft.icons.PAID, "index": 9},
                    # {"label": "Home", "icon": ft.icons.MONETIZATION_ON, "index": 10},
                    {"label": "Importar XML", "icon": ft.icons.RECEIPT, "index": 11},
                ],
            },
            {
                "title": "Outras Opções",
                "subtitle": "Mais funcionalidades",
                "collapsed_text_color": ft.Colors.YELLOW,
                "items": [
                    {"label": "Configurações", "icon": ft.icons.SETTINGS, "index": 999},
                    {"label": "Ajuda", "icon": ft.icons.HELP, "index": 998},
                ],
            },
        ]

        self.build_drawer()

    def build_drawer(self):
        """Cria os ExpansionTiles dinamicamente com base nos grupos."""
        self.controls.clear()  # Limpa os controles atuais
        self.expansion_states = [False] * len(self.groups)  # Inicializa os estados como fechados
        self.controls.append(ft.Container(height=12))  # Espaçamento inicial
        self.controls.append(
            ft.Image(
                src="images\\logo_lins.png",
                width=100,
                height=200,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )  # Imagem inicial
        self.controls.append(ft.Divider(thickness=2))  # Espaçamento inicial

        for i, group in enumerate(self.groups):
            expansion_tile = ft.ExpansionTile(
                title=ft.Text(group["title"]),
                subtitle=ft.Text(group["subtitle"]),
                affinity=ft.TileAffinity.PLATFORM,
                maintain_state=False,
                expand=self.expansion_states[i],  # Define o estado inicial
                collapsed_text_color=group["collapsed_text_color"],
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(item["icon"]),
                        title=ft.Text(item["label"]),
                        on_click=lambda e, idx=item["index"]: self._on_tile_click(idx),
                    )
                    for item in group["items"]
                ],
            )

            # Associa o índice atual diretamente ao evento
            expansion_tile.on_change = lambda e, idx=i: self._handle_expansion_tile(idx)
            self.controls.append(expansion_tile)

    def _handle_expansion_tile(self, index, e=None):
        """Fecha todos os ExpansionTiles, exceto o selecionado."""
        self.expansion_states = [i == index for i in range(len(self.groups))]

        tile_index = 0
        for control in self.controls:
            if isinstance(control, ft.ExpansionTile):
                control.expand = self.expansion_states[tile_index]
                tile_index += 1

        # Verifica se o componente foi adicionado à página
        if self.page:
            self.update()  # Atualiza a interface
        else:
            print("Erro: MyNavigationDrawer não está anexado à página.")


    def _on_tile_click(self, index):
        """Atualiza o índice selecionado e chama o callback `on_change`."""
        self.selected_index = index
        if self.on_change:
            self.on_change(self)

