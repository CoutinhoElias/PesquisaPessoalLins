from partials.all_imports import * 
# from region_detail import *
from partials.region_detail import field_tipos

tf_norte_eletricos_simples, tf_norte_eletricos_importados, tf_norte_eletricos_demais = field_tipos()
tf_norte_informatica_simples, tf_norte_informatica_importados, tf_norte_informatica_demais = field_tipos()
# tf_norte_eletricos_simples.bgcolor=ft.colors.BLACK

tf_nordeste_eletricos_simples, tf_nordeste_eletricos_importados, tf_nordeste_eletricos_demais = field_tipos()
tf_nordeste_informatica_simples, tf_nordeste_informatica_importados, tf_nordeste_informatica_demais = field_tipos()

tf_ceara_eletricos_simples, tf_ceara_eletricos_importados, tf_ceara_eletricos_demais = field_tipos()
tf_ceara_informatica_simples, tf_ceara_informatica_importados, tf_ceara_informatica_demais = field_tipos()

tf_centro_oeste_eletricos_simples, tf_centro_oeste_eletricos_importados, tf_centro_oeste_eletricos_demais = field_tipos()
tf_centro_oeste_informatica_simples, tf_centro_oeste_informatica_importados, tf_centro_oeste_informatica_demais = field_tipos()

tf_sudeste_eletricos_simples, tf_sudeste_eletricos_importados, tf_sudeste_eletricos_demais = field_tipos()
tf_sudeste_informatica_simples, tf_sudeste_informatica_importados, tf_sudeste_informatica_demais = field_tipos()

tf_sul_eletricos_simples, tf_sul_eletricos_importados, tf_sul_eletricos_demais = field_tipos()
tf_sul_informatica_simples, tf_sul_informatica_importados, tf_sul_informatica_demais = field_tipos()

# Mesmo tipo dos TFs acima mas aqui com outro propósito.
# ir_fat, margem_lucro_esperado, finan
ir_fat = ft.TextField(
    label="IR/FAT", 
    hint_text="IR/FAT",
    col={"md": 2}, 
    # on_blur=lambda event: alteracao(event.control.value), 
    focused_border_color = ft.colors.GREEN,
    # input_filter=ft.NumbersOnlyInputFilter(),
)

margem_lucro_esperado = ft.TextField(
    label="Margem de Lucro Esperado", 
    hint_text="Margem de Lucro Esperado",
    col={"md": 2}, 
    # on_blur=lambda event: alteracao(event.control.value), 
    focused_border_color = ft.colors.GREEN,
    # input_filter=ft.NumbersOnlyInputFilter(),
)

finan = ft.TextField(
    label="Finan", 
    hint_text="Finan",
    col={"md": 2}, 
    # on_blur=lambda event: alteracao(event.control.value), 
    focused_border_color = ft.colors.GREEN,
    # input_filter=ft.NumbersOnlyInputFilter(),
)

fields_norte = ft.Ref[ft.ResponsiveRow]
fields_sul = ft.Ref[ft.ResponsiveRow]
fields_sudeste = ft.Ref[ft.ResponsiveRow]
fields_ceara = ft.Ref[ft.ResponsiveRow]
fields_centro_oeste = ft.Ref[ft.ResponsiveRow]

def handle_expansion_tile_change(e):
    print(e.control.controls[3])

def region_tile():
    norte = ft.ExpansionTile(
        title=ft.Text("Região Norte", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Edite tudo por Região"),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        collapsed_text_color=ft.colors.GREEN,
        text_color=ft.colors.GREEN,
        # bgcolor=ft.colors.GREEN,
        controls_padding=5,
        on_change=handle_expansion_tile_change,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                ref=fields_norte,
                controls=                 
                [
                    tf_norte_eletricos_simples, tf_norte_eletricos_importados, tf_norte_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    tf_norte_informatica_simples, tf_norte_informatica_importados, tf_norte_informatica_demais
                ],
                run_spacing={"xs": 12},
            ), 

        ],
    )

    nordeste = ft.ExpansionTile(
        title=ft.Text("Região Nordeste", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Está incluso estado do Espirito Santo, excluindo Ceará"),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        collapsed_text_color=ft.colors.RED,
        text_color=ft.colors.RED,
        # on_change=handle_expansion_tile_change,
        controls_padding=5,
        # ref=ref_nordeste,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                # ref=fields_nordeste,
                controls=                 
                [
                    tf_nordeste_eletricos_simples, tf_nordeste_eletricos_importados, tf_nordeste_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    tf_nordeste_informatica_simples, tf_nordeste_informatica_importados, tf_nordeste_informatica_demais
                ],
                run_spacing={"xs": 12},
            ), 
        ],
    )

    ceara = ft.ExpansionTile(
        title=ft.Text("Região do Ceará", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Sendo tratado como Região"),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        # initially_expanded=True,
        collapsed_text_color=ft.colors.RED_ACCENT_100,
        text_color=ft.colors.RED_ACCENT_100,
        controls_padding=5,
        # ref=ref_ceara,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                ref=fields_ceara,
                controls=                 
                [
                    tf_ceara_eletricos_simples, tf_ceara_eletricos_importados, tf_ceara_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    tf_ceara_informatica_simples, tf_ceara_informatica_importados, tf_ceara_informatica_demais
                ],
                run_spacing={"xs": 12},
            ),
        ],
    )

    centro_oeste = ft.ExpansionTile(
        title=ft.Text("Região Centro-Oeste", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Edite tudo por Região"),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        # initially_expanded=True,
        collapsed_text_color=ft.colors.BROWN,
        text_color=ft.colors.BROWN,
        controls_padding=5,
        # ref=ref_centro_oeste,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                ref=fields_centro_oeste,
                controls=                 
                [
                    tf_centro_oeste_eletricos_simples, tf_centro_oeste_eletricos_importados, tf_centro_oeste_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    tf_centro_oeste_informatica_simples, tf_centro_oeste_informatica_importados, tf_centro_oeste_informatica_demais
                ],
                run_spacing={"xs": 12},
            ),
        ],
    )

    sudeste = ft.ExpansionTile(
        title=ft.Text("Região Sudeste", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Edite tudo por Região"),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        # initially_expanded=True,
        collapsed_text_color=ft.colors.GREEN_ACCENT_100,
        text_color=ft.colors.GREEN_ACCENT_100,
        controls_padding=5,
        # ref=ref_sudeste,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                ref=fields_sudeste,
                controls=                 
                [
                    tf_sudeste_eletricos_simples, tf_sudeste_eletricos_importados, tf_sudeste_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    tf_sudeste_informatica_simples, tf_sudeste_informatica_importados, tf_sudeste_informatica_demais
                ],
                run_spacing={"xs": 12},
            ),
        ],
    )

    sul = ft.ExpansionTile(
        title=ft.Text("Região Sul", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Edite tudo por Região"),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        # initially_expanded=True,
        collapsed_text_color=ft.colors.BLUE,
        text_color=ft.colors.BLUE,
        controls_padding=5,
        # ref=ref_sudeste,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                ref=fields_sul,
                controls=                 
                [
                    tf_sul_eletricos_simples, tf_sul_eletricos_importados, tf_sul_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    tf_sul_informatica_simples, tf_sul_informatica_importados, tf_sul_informatica_demais
                ],
                run_spacing={"xs": 12},
            ),
        ],
    )

    dados_custo = ft.ExpansionTile(
        title=ft.Text("Informações para custo", weight=ft.FontWeight.BOLD,),
        subtitle=ft.Text("Ajustes de cálculo de custo."),
        affinity=ft.TileAffinity.PLATFORM,
        maintain_state=True,
        # initially_expanded=True,
        collapsed_text_color=ft.colors.BLUE,
        text_color=ft.colors.BLUE,
        controls_padding=5,
        # ref=ref_sudeste,
        controls=[
            ft.ListTile(title=ft.Text("Valores para Produtos Elétricos:")),
            ft.ResponsiveRow(
                ref=fields_sul,
                controls=                 
                [
                    tf_sul_eletricos_simples, tf_sul_eletricos_importados, tf_sul_eletricos_demais
                ],
                run_spacing={"xs": 12},
            ),

            ft.ListTile(title=ft.Text("Valores para Produtos Informática:")),
            ft.ResponsiveRow(
                [
                    ir_fat, margem_lucro_esperado, finan
                ],
                run_spacing={"xs": 12},
            ),
        ],
    )
    return norte, nordeste, ceara, centro_oeste, sudeste, sul