import flet as ft

class MyButton(ft.ElevatedButton):
    def __init__(self, text, on_click, bgcolor=ft.colors.ORANGE_300, expand=True):
        super().__init__()
        self.bgcolor = bgcolor  # Usa a cor passada ou a cor padrão
        self.color = ft.colors.BLACK
        self.text = text
        self.expand = expand  # Permite que o valor seja definido externamente
        self.on_click = on_click



# # Usando a cor padrão
# button1 = MyButton(text="Clique aqui", on_click=lambda e: print("Botão clicado!"))

# # Usando uma cor personalizada
# button2 = MyButton(text="Clique aqui", on_click=lambda e: print("Botão clicado!"), bgcolor=ft.colors.BLUE_300)