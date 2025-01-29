# import os
# import pymssql

# USER = os.getenv('DB_USER', 'sa')
# PASSWORD = os.getenv('DB_PASSWORD', 'Abc*123')
# HOST = os.getenv('DB_HOST', '192.168.254.1')
# DATABASE = os.getenv('DB_NAME', 'ALTERDATA_TESTE')

# # Configuração da conexão
# connection_string = f'mssql+pymssql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

# from sqlalchemy import create_engine, text, Column, update, insert, select, desc, func, and_
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import text

# engine = create_engine(connection_string)
# Session = sessionmaker(bind=engine)
# session = Session()



# def execute_stored_procedure(entity, column, value):
#     result = session.execute(text("EXEC stp_GetMultiCode :entity, :column, :value"),
#                             {'entity': entity, 
#                                 'column': column, 
#                                 'value': value})
#     return result

# result = execute_stored_procedure('PedidoDeCompra', 'IdPedidoDeCompra', 1)
# for row in result:
#     print(row)

# session.close()






# import pymssql

# # Configuração da conexão
# USER = 'sa'
# PASSWORD = 'Abc*123'
# HOST = '192.168.254.1'
# DATABASE = 'ALTERDATA_TESTE'

# # Função para executar a stored procedure com pymssql
# def execute_stored_procedure():
#     try:
#         # Conecta ao banco de dados
#         with pymssql.connect(server=HOST, user=USER, password=PASSWORD, database=DATABASE) as conn:
#             with conn.cursor() as cursor:
#                 # Chama a stored procedure com parâmetros de entrada e captura o de saída
#                 cursor.execute("""
#                     DECLARE @OutputParam INT;
#                     EXEC stp_GetMultiCode @TableName = %s, @FieldName = %s, @NrCodigos = %s;
#                 """, ('PedidoDeCompra', 'IdPedidoDeCompra', 1))

#                 # Captura o valor retornado
#                 output_value = cursor.fetchall()  # fetchall() para múltiplos códigos, caso a stored procedure retorne mais de um

#                 # Verifica se há resultados
#                 if output_value:
#                     print("Output Param:", output_value)
#                 else:
#                     print("Nenhum código retornado.")

#                 # Retorna os resultados
#                 return output_value

#     except pymssql.DatabaseError as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return None

# # Executa a função
# result = execute_stored_procedure()

# # Exibe os resultados
# print(result)





# import pymssql

# # Configuração da conexão
# USER = 'sa'
# PASSWORD = 'Abc*123'
# HOST = '192.168.254.1'
# DATABASE = 'ALTERDATA_TESTE'

# # Função para executar a stored procedure com pymssql
# def execute_stored_procedure(entity, column, value):
#     try:
#         # Conecta ao banco de dados
#         with pymssql.connect(server=HOST, user=USER, password=PASSWORD, database=DATABASE) as conn:
#             with conn.cursor() as cursor:
#                 # Executa a stored procedure diretamente com callproc
#                 cursor.callproc('stp_GetMultiCode', (entity, column, value))

#                 # Recupera os resultados da primeira tabela retornada
#                 result = cursor.fetchall()
                
#                 # Retorna os resultados
#                 return result
#     except pymssql.DatabaseError as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return None

# # Executa a função
# result = execute_stored_procedure('PedidoDeCompra', 'IdPedidoDeCompra', 1)

# # Exibe os resultados
# for row in result:
#     print(row)


# ---------------------------------------------------------------------------------------------------------------
# import flet as ft

# def main(page):
#     # Configurando o modo claro para o tema da página
#     page.theme_mode = ft.ThemeMode.LIGHT

#     # Função que será chamada ao carregar o arquivo
#     def on_upload(e):
#         # Mostrando o nome do arquivo carregado
#         uploaded_file = e.files[0]
#         page.add(ft.Text(f"Arquivo carregado: {uploaded_file.name}"))

#     # Função para simular o carregamento do arquivo
#     def start_upload(e):
#         # Indicador de atividade enquanto o upload está ocorrendo
#         upload_indicator = ft.CupertinoActivityIndicator(radius=50, color=ft.colors.RED, animating=True)
#         page.add(upload_indicator)
        
#         # Simulando o tempo de upload
#         page.update()  # Atualizando a página para exibir o indicador de atividade
#         page.snack_bar = ft.SnackBar(ft.Text("Carregando arquivo..."))
#         page.snack_bar.open = True
#         page.update()

#         # Simulando uma espera para o "upload"
#         import time
#         time.sleep(2)

#         # Removendo o indicador de atividade após o upload
#         page.remove(upload_indicator)
#         page.snack_bar.open = False
#         page.update()

#     # Botão para selecionar o arquivo e iniciar o upload
#     file_picker = ft.FilePicker(on_result=on_upload)
#     page.overlay.append(file_picker)

#     page.add(
#         ft.Column(
#             controls=[
#                 ft.ElevatedButton("Selecionar Arquivo", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files()),
#                 ft.ElevatedButton("Iniciar Upload", on_click=start_upload),
#             ]
#         )
#     )

# # Iniciando a aplicação
# ft.app(target=main)
# ------------------------------------------------------------------------------------------------------------------
# import flet as ft

# def main(page: ft.Page):
#     page.add(
#         ft.DataTable(
#         width=700,
#         bgcolor="yellow",
#         border=ft.border.all(2, "red"),
#         border_radius=10,
#         vertical_lines=ft.BorderSide(3, "blue"),
#         horizontal_lines=ft.BorderSide(1, "green"),
#         sort_column_index=0,
#         sort_ascending=True,
#         heading_row_color=ft.colors.BLACK12,
#         heading_row_height=100,
#         data_row_color={"hovered": "0x30FF0000"},
#         show_checkbox_column=True,
#         divider_thickness=0,
#         column_spacing=200,
#         columns=[
#             ft.DataColumn(
#                 ft.Text("Column 1"),
#                 on_sort=lambda e: [# Select the column itself
#                                    e.control.parent.__setattr__("sort_column_index" , e.column_index) ,
#                                    # Toggle the sort (ascending / descending)
#                                    e.control.parent.__setattr__("sort_ascending" , False) if e.control.parent.sort_ascending else e.control.parent.__setattr__("sort_ascending" , True) ,
#                                    # Sort the table rows according above
#                                    e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value,reverse = e.control.parent.sort_ascending) ,
#                                    # Update table
#                                    e.control.parent.update()
#                                   ],
#             ),
#             ft.DataColumn(
#                 ft.Text("Column 2"),
#                 tooltip="This is a second column",
#                 numeric=True,
#                 on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
#             ),
#         ],
#         rows=[
#             ft.DataRow(
#                 [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#                 selected=True,
#                 on_select_changed=lambda e: print(f"row select changed: {e.data}"),
#             ),
#             ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
#         ],
#     ),
# )

# ft.app(target=main)
# ------------------------------------------------------------------------------------------------------------------

# import flet as ft

# def main(page: ft.Page):

#     # Dados iniciais da tabela
#     data = [
#         ["Ana", 25, "Engenheira"],
#         ["Bruno", 30, "Designer"],
#         ["Carlos", 22, "Desenvolvedor"],
#         ["Daniela", 28, "Gerente"],
#     ]

#     # Estado para controle da ordenação
#     ascending = True

#     # Função que reordena as linhas com base na coluna clicada
#     def sort_table(e, column_index):
#         nonlocal ascending, data
#         data.sort(key=lambda x: x[column_index], reverse=not ascending)
#         ascending = not ascending
#         update_table()

#     # Função para atualizar a tabela
#     def update_table():
#         table.rows.clear()

#         for row in data:
#             table.rows.append(ft.DataRow(cells=[
#                 ft.DataCell(ft.Text(row[0])),
#                 ft.DataCell(ft.Text(str(row[1]))),
#                 ft.DataCell(ft.Text(row[2])),
#             ]))
            
#         page.update()

#     # Definindo a tabela
#     table = ft.DataTable(
#         columns=[
#             ft.DataColumn(ft.Text("Nome"), on_sort=lambda e: sort_table(e, 0)),
#             ft.DataColumn(ft.Text("Idade"), on_sort=lambda e: sort_table(e, 1)),
#             ft.DataColumn(ft.Text("Profissão"), on_sort=lambda e: sort_table(e, 2)),
#         ],
#         rows=[]
#     )

#     # Carregando os dados iniciais na tabela
#     update_table()

#     # Adicionando a tabela à página
#     page.add(table)

# ft.app(target=main)
# ------------------------------------------------------------------------------------------------------------------
# EXEMPLO DE DATATABLE IMPLEMENTADO USO DE CHECKBOX SEPARADO NA COLUNA, POSSIBILITANDO EDITAR DADO DA CELULA.
# import flet as ft

# def main(page: ft.Page):
#     # Lista para armazenar o estado de cada checkbox na tabela
#     checkbox_states = [False, False]

#     # Função para atualizar o estado de todos os checkboxes na tabela
#     def toggle_all_checkboxes(e):
#         is_checked = e.control.value
#         for i in range(len(checkbox_states)):
#             checkbox_states[i] = is_checked
#             # Atualiza o valor de cada checkbox no DataRow
#             page.controls[0].rows[i].cells[0].content.value = is_checked
#             page.controls[0].rows[i].cells[0].content.update()
#         print(f"Todos os checkboxes foram {'marcados' if is_checked else 'desmarcados'}.")

#     # Função chamada ao alterar o estado de um checkbox individual
#     def checkbox_changed(e, index):
#         checkbox_states[index] = e.control.value
#         print(f"Checkbox da linha {index+1} {'marcado' if e.control.value else 'desmarcado'}.")

#         # Se um checkbox individual for desmarcado, desmarca o checkbox de "marcar todos"
#         if not e.control.value:
#             page.controls[0].columns[0].label.value = False
#             page.controls[0].columns[0].label.update()
#         else:
#             # Se todos os checkboxes forem marcados, marca o checkbox do cabeçalho
#             if all(checkbox_states):
#                 page.controls[0].columns[0].label.value = True
#                 page.controls[0].columns[0].label.update()

#     # Cria a DataTable
#     page.add(
#         ft.DataTable(
#             width=700,
#             bgcolor="yellow",
#             border=ft.border.all(2, "red"),
#             border_radius=10,
#             vertical_lines=ft.BorderSide(3, "blue"),
#             horizontal_lines=ft.BorderSide(1, "green"),
#             sort_column_index=0,
#             sort_ascending=True,
#             heading_row_color=ft.colors.BLACK12,
#             heading_row_height=100,
#             data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
#             show_checkbox_column=False,  # Desabilitar o checkbox padrão
#             divider_thickness=0,
#             column_spacing=200,
#             columns=[
#                 ft.DataColumn(
#                     ft.Checkbox(
#                         value=False, on_change=toggle_all_checkboxes
#                     ),  # Checkbox no cabeçalho
#                     on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
#                 ),
#                 ft.DataColumn(
#                     ft.Text("Coluna 1"),
#                 ),
#                 ft.DataColumn(
#                     ft.Text("Coluna 2"),
#                     numeric=True,
#                 ),
#             ],
#             rows=[
#                 ft.DataRow(
#                     [
#                         ft.DataCell(ft.Checkbox(value=False, on_change=lambda e: checkbox_changed(e, 0))),  # Checkbox individual
#                         ft.DataCell(ft.Text("A")),
#                         ft.DataCell(ft.Text("1")),
#                     ],
#                 ),
#                 ft.DataRow(
#                     [
#                         ft.DataCell(ft.Checkbox(value=False, on_change=lambda e: checkbox_changed(e, 1))),  # Checkbox individual
#                         ft.DataCell(ft.Text("B")),
#                         ft.DataCell(ft.Text("2")),
#                     ],
#                 ),
#             ],
#         )
#     )

# ft.app(main)
# ------------------------------------------------------------------------------------------------------------------


from time import sleep

import flet as ft

def main(page: ft.Page):
    pb = ft.ProgressBar(width=400)

    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ ft.Text("Doing something..."), pb]),
        # ft.Text("Indeterminate progress bar", style="headlineSmall"),
        # ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
    )

    for i in range(0, 101):
        pb.value = i * 0.01
        sleep(0.1)
        page.update()

ft.app(main)


# import flet as ft

# def main(page: ft.Page):

#     # Imagem arredondada diretamente no botão, com bordas arredondadas
#     image_in_button = ft.Image(
#         src="C:\\Users\\SV\\Documents\\codes_sv\\Curso\\assets\\images\\excel.jpg",  # Caminho da imagem
#         fit=ft.ImageFit.COVER,
#         width=40,  # Ajuste o tamanho da imagem
#         height=40,
#         border_radius=ft.border_radius.all(20)  # Deixa a imagem arredondada
#     )

#     # Adicionando a imagem diretamente ao ElevatedButton
#     button_with_image = ft.ElevatedButton(
#         content=image_in_button,
#         on_click=lambda e: print("Botão com imagem arredondada clicado!")
#     )

#     # Adicionando a imagem arredondada no ListTile
#     list_tile_with_image = ft.ListTile(
#         leading=image_in_button,  # Substitui o ícone por uma imagem arredondada
#         title=ft.Text("Importar Planilha"),
#         subtitle=ft.Text("Clique para importar os dados"),
#         on_click=lambda e: print("ListTile com imagem arredondada clicado!")
#     )

#     # Teste de imagem separada para visualização
#     image_test = ft.Image(
#         src="C:\\Users\\SV\\Documents\\codes_sv\\Curso\\assets\\images\\excel.jpg",
#         fit=ft.ImageFit.CONTAIN,
#         width=50,
#         height=50,
#         border_radius=ft.border_radius.all(25),
#     )

#     # Adicionando à página
#     page.add(button_with_image, list_tile_with_image, image_test)

# # Inicializa o aplicativo Flet
# ft.app(target=main)

# ------------------------------------------------------------------------------------------------------------------
# Tabela
# import flet as ft

# class CustomDataTable:
#     def __init__(self, colunas, linhas):
#         self.colunas = colunas
#         self.linhas = linhas
#         self.checkbox_states = [False] * len(linhas)  # Estados dos checkboxes individuais
#         self.data_table = None  # Inicialização da tabela

#     def toggle_all_checkboxes(self, e):
#         is_checked = e.control.value
#         for i in range(len(self.checkbox_states)):
#             self.checkbox_states[i] = is_checked
#             self.data_table.rows[i].cells[0].content.value = is_checked
#             self.data_table.rows[i].cells[0].content.update()
#             self.data_table.update()  # Add this line to update the table
#         print(f"Todos os checkboxes foram {'marcados' if is_checked else 'desmarcados'}.")

#     def checkbox_changed(self, e, index):
#         self.checkbox_states[index] = e.control.value
#         print(f"Checkbox da linha {index+1} {'marcado' if e.control.value else 'desmarcado'}.")
#         if not e.control.value:
#             self.data_table.columns[0].label.value = False
#             self.data_table.columns[0].label.update()
#         else:
#             if all(self.checkbox_states):
#                 self.data_table.columns[0].label.value = True
#                 self.data_table.columns[0].label.update()
#         self.data_table.update()  # Add this line to update the table

#     # Função para ordenar as colunas
#     def sort_column(self, e):
#         column_index = e.column_index
#         self.data_table.sort_ascending = not self.data_table.sort_ascending
#         if column_index == 0:
#             self.data_table.rows.sort(key=lambda x: x.cells[column_index].content.value, reverse=not self.data_table.sort_ascending)
#             self.checkbox_states = [row.cells[0].content.value for row in self.data_table.rows]  # Update checkbox_states
#         else:
#             self.data_table.rows.sort(key=lambda x: x.cells[column_index].content.value, reverse=not self.data_table.sort_ascending)
#         self.data_table.update()


#     def criar_data_table(self, ref=None):
#         # Cria a tabela com as colunas e as funções dos checkboxes
#         self.data_table = ft.DataTable(
#             data_row_max_height=25,
#             border=ft.border.all(2, "red"),
#             border_radius=10,
#             vertical_lines=ft.BorderSide(3, "blue"),
#             horizontal_lines=ft.BorderSide(1, "green"),
#             sort_column_index=0,
#             sort_ascending=True,
#             heading_row_color=ft.colors.BLACK12,
#             heading_row_height=55,
#             data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
#             show_checkbox_column=False,  # Desabilitar o checkbox padrão
#             divider_thickness=0,
#             data_row_min_height=15,  # Ajuste da altura mínima das linhas
#             columns=[
#                 ft.DataColumn(
#                     ft.Checkbox(
#                         value=False, on_change=self.toggle_all_checkboxes  # Checkbox no cabeçalho
#                     ), on_sort=self.sort_column  # Permitir ordenação pelos checkboxes
#                 )
#             ] + [ft.DataColumn(col.label, on_sort=self.sort_column) for col in self.colunas],  # Adiciona as colunas extras com suporte à ordenação
#             rows=[
#                 ft.DataRow(
#                     [
#                         ft.DataCell(ft.Checkbox(value=False, on_change=lambda e, idx=i: self.checkbox_changed(e, idx))),
#                     ] + row,  # Adiciona os checkboxes nas linhas
#                 )
#                 for i, row in enumerate(self.linhas)
#             ]
#         )
#         return self.data_table  # Retorna a DataTable pronta

# def main(page: ft.Page):
#     page.theme_mode = "dark"  # Define o tema como escuro
#     page.window.center()  # Centraliza a janela na tela

#     # Definindo colunas e linhas externas
#     colunas_dos_itens_dos_pedidos = [
#         ft.DataColumn(ft.Text("Coluna 1", width=460)),
#         ft.DataColumn(ft.Text("Coluna 2", width=50), numeric=True),
#     ]
    
#     linhas_dos_itens_dos_pedidos = [
#         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#         [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
#         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#         [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
#         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#         [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
#         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#         [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
#         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#         [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
#         [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
#     ]
#     print(type(linhas_dos_itens_dos_pedidos), '*****')
#     # Instanciando a classe
#     custom_table = CustomDataTable(colunas_dos_itens_dos_pedidos, linhas_dos_itens_dos_pedidos)
    
#     # Adicionando a tabela pronta na página
#     page.add(custom_table.criar_data_table())

# ft.app(main)


# ------------------------------------------------------------------------------------------------------------------

# from time import sleep
# import flet as ft

# def main(page: ft.Page):
#     def button_click(e):
#         loading = ft.AlertDialog(
#             content=ft.Container(
#                 content=ft.ProgressRing(),
#                 alignment=ft.alignment.center,
#             ),
#             bgcolor=ft.colors.TRANSPARENT,
#             modal=True,
#             disabled=True,
#         )
#         page.open(loading)
#         sleep(3)
#         page.close(loading)

#     btn = ft.ElevatedButton("Executar tarefa!", on_click=button_click)
#     page.add(btn)

# ft.app(target=main)


# ------------------- FUNCIONANDO -----------------------------------------
# import pyodbc

# # Configuração da conexão
# USER = 'sa'
# PASSWORD = 'Abc*123'
# HOST = '192.168.254.1'
# DATABASE = 'ALTERDATA_TESTE'

# # String de conexão
# connection_string = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     f'SERVER={HOST};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
# )

# # Função para executar a stored procedure com pyodbc
# def execute_stored_procedure(entity, column, value):
#     try:
#         # Conecta ao banco de dados
#         with pyodbc.connect(connection_string) as conn:
#             with conn.cursor() as cursor:
#                 # Executa a stored procedure diretamente
#                 cursor.execute("{CALL stp_GetMultiCode(?, ?, ?)}", (entity, column, value))
                
#                 # Recupera os resultados
#                 result = cursor.fetchall()
#                 return result
#     except pyodbc.DatabaseError as e:
#         print(f"Erro ao acessar o banco de dados: {e}")
#         return None

# # Executa a função
# result = execute_stored_procedure('PedidoDeCompra', 'IdPedidoDeCompra', 1)

# # Exibe os resultados
# for row in result:
#     print(row)

