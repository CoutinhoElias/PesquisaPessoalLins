from partials.all_imports import *

def field_tipos():
    # def alteracao(event):
    #     print("Evento de alteração acionado!")
    #     print(unificado)
    #     # Aqui você pode adicionar a lógica desejada para o evento de alteração
            
    fator_simples = ft.TextField(
        label="Fator para Simples", 
        hint_text="SIMPLES NACIONAL", 
        col={"md": 2}, 
        # on_blur=lambda event: alteracao(event.control.value), 
        focused_border_color = ft.colors.GREEN,
        # input_filter=ft.NumbersOnlyInputFilter(),
    )

    fator_importados = ft.TextField(
        label="Fator para Importado", 
        hint_text="IMPORTADOS",
        # height=50, 
        col={"md": 2},
        # on_blur=lambda event: identificar_produto(event.control.value), 
        # disabled=True,
        focused_border_color = ft.colors.YELLOW,
        # input_filter=ft.NumbersOnlyInputFilter()
    )

    fator_demais_produtos = ft.TextField(
        label="Fator padrão", 
        hint_text="DEMAIS PRODUTOS",
        # height=50, 
        col={"md": 2},
        # on_blur=lambda event: o(event.control.value), 
        # disabled=True,
        focused_border_color = ft.colors.BLUE,
        # input_filter=ft.NumbersOnlyInputFilter()
    )
    return fator_simples, fator_importados, fator_demais_produtos
