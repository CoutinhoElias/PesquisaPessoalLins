import flet as ft
from partials.button import MyButton

class HomeView:
    # def __init__(self, page: ft.Page, app_instance):

    #     super().__init__()
    #     self.page = page  # Certifique-se de armazenar a página na instância
    #     self.app_instance = app_instance  # Armazena a referência para a instância da classe App

    def get_content(self):
        # def ok_clicked(e):
        #     print("OK clicked")

        # button = MyButton(text="OK", on_click=ok_clicked)
        # text = ft.Text(value="Bem-vindo à Home!", color=ft.colors.WHITE)
        dash = ft.Image(
                        src=f"images\dash.png",
                        # width=100,
                        # height=100,
                        # fit=ft.ImageFit.CONTAIN,
                        expand=True
                        )
        
        # layout = ft.Column(
        #     controls=[
        #         dash
        #     ],
        #     alignment=ft.alignment.center,
        #     expand=True
        # )

        layout = ft.ResponsiveRow(
            columns=12,
            controls=[
                dash
            ],
            expand=True
        )        
        return layout
