import flet as ft
# from partials.all_imports import *
# from partials.all_imports import Session
# from partials.ler_nfe import *
from partials.all_imports import Session # <<<<<===================================
from configs.alterdata_api_base_connection import BaseConnection
from partials.data_table_person import create_datatable, my_table, sort_column
from partials.button import MyButton
from database.models import LoteDoc, LoteDocItem

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import update
import asyncio
from asyncio import sleep

from partials.ler_nfe import LerNFE

import requests
import json
# Definir a localização como "Português do Brasil"
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

from datetime import datetime

# Função para formatar a data atual
def format_current_date():
    data = datetime.now()
    return data.strftime('%Y-%m-%d 00:00:00.000')

# Data formatada
data_formatada = format_current_date()

''' Criei uma classe chamada BaseConnection que será herdada pelas minhas classes
que usarem o super().__init__().
'''
class PedidoDeVendaVW(BaseConnection):
    def __init__(self, page: ft.Page, app_instance):
        super().__init__()

        self.page = page
        self.tabela_ref = ft.Ref[ft.DataTable]()

        self.ler_nfe = LerNFE()
        self.page.add(self.progress_bar)  # Adiciona a barra de progresso à página

        # Inicialização do FilePicker e texto para exibir arquivos selecionados
        self.selected_files = ft.Text()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)

        self.outras_despesas = 0

        # Construção da TABELA
        # =========================================================================================================================================
        # Definição do Ref().
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
        self.tb_tab_pedido = ft.Ref[ft.Tab]()

        # ============================================================================================================================= 

        # LISTA DE ITENS DA TABELA
        self.colunas_itens = [
            ft.DataColumn(ft.Text("Código", width=50), on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Descricao", width=70), on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Qde", width=60), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Unitário", width=60), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Total", width=60), numeric=True, on_sort=lambda e: sort_column(e)),
        ]

        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.colunas_itens)
        self.table_order_items = my_table(self.datatable_itens_pedido)
        # =========================================================================================================================================

        self.botao_criar = MyButton(text="Criar Pedido", on_click=self.criar_pedido, bgcolor=ft.Colors.BLUE_300, expand=True)

        # self.dados_tabela = []
        self.dialogo = ft.AlertDialog(
            title=ft.Text(value="Mensagem do Sistema"),
            content=ft.Text(value="Nenhuma ação foi realizada."),
            title_padding=ft.padding.all(10),
            content_padding=ft.padding.all(10),
            shape=ft.RoundedRectangleBorder(radius=5),
        )

    # def atualizar_itens_pedidos(self, id_pedido_de_venda):
    #     # session = create_session()
    #     valor_capa = 0
    #     try:
    #         for chave, produto in self.dados_nfe_xml['produtos'].items():
    #             self.outras_despesas = self.outras_despesas + float(produto['valor_frete'])
    #             if "IPI" in produto['impostos']:
    #                 id_produto = produto['IdProduto']
    #                 ipi = produto['impostos']["IPI"]
    #                 base_calculo = float(ipi["vBC"])
    #                 aliquota = float(ipi["pIPI"])
    #                 valor = float(ipi["vIPI"])

    #                 valor_capa = valor_capa + base_calculo + valor

    #                 # Consulta de atualização
    #                 session.execute(
    #                     update(LoteDocItem)
    #                     .where(LoteDocItem.IdDocumento == id_pedido_de_venda, LoteDocItem.IdProduto == id_produto)
    #                     .values(
    #                         AlICMS=0,
    #                         VlBaseIPI=base_calculo,
    #                         AlIPI=aliquota,
    #                         VlIPI=valor,
    #                         CdSituacaoTributariaIPI='00',
    #                         CdEnquadramentoLegalIPI='999'
    #                     )
    #                 )

    #             session.execute(
    #                 update(LoteDocItem)
    #                 .where(LoteDocItem.IdDocumento == id_pedido_de_venda)
    #                 .values(
    #                     AlICMS=None,
    #                 )
    #             )
                
    #         session.commit()
    #         return valor_capa
    #         print("Atualização concluída com sucesso.")
    #     except SQLAlchemyError as e:
    #         session.rollback()
    #         print("Erro ao atualizar o banco de dados:", str(e))
    #     finally:
    #         # self.dados_nfe_xml.clear()
    #         # self.ler_nfe.itens.clear()  # Clear self.itens            
    #         session.close()
  

    def atualizar_itens_pedidos(self, id_pedido_de_venda):
        # Session = sessionmaker(bind=engine)  # Supondo que `engine` seja a sua conexão com o banco de dados
        valor_capa = 0

        with Session() as session:
            try:
                for chave, produto in self.dados_nfe_xml['produtos'].items():
                    self.outras_despesas = self.outras_despesas + float(produto['valor_frete'])
                    if "IPI" in produto['impostos']:
                        id_produto = produto['IdProduto']
                        ipi = produto['impostos']["IPI"]
                        base_calculo = float(ipi["vBC"])
                        aliquota = float(ipi["pIPI"])
                        valor = float(ipi["vIPI"])

                        valor_capa = valor_capa + base_calculo + valor

                        # Consulta de atualização
                        session.execute(
                            update(LoteDocItem)
                            .where(LoteDocItem.IdDocumento == id_pedido_de_venda, LoteDocItem.IdProduto == id_produto)
                            .values(
                                AlICMS=0,
                                VlBaseIPI=base_calculo,
                                AlIPI=aliquota,
                                VlIPI=valor,
                                CdSituacaoTributariaIPI='00',
                                CdEnquadramentoLegalIPI='999'
                            )
                        )

                    session.execute(
                        update(LoteDocItem)
                        .where(LoteDocItem.IdDocumento == id_pedido_de_venda)
                        .values(
                            AlICMS=None,
                        )
                    )

                session.commit()
                print("Atualização concluída com sucesso.")
                return valor_capa

            except SQLAlchemyError as e:
                session.rollback()
                print("Erro ao atualizar o banco de dados:", str(e))
                raise  # Re-lança a exceção para que o chamador possa lidar com ela, se necessário


    def atualizar_capa_pedidos(self, id_pedido_de_venda, total):
        with Session() as session:
            try:
                # Consulta de atualização
                session.execute(
                    update(LoteDoc)
                    .where(LoteDoc.IdDocumento == id_pedido_de_venda)
                    .values(
                        VlDocumento=total,
                        VlOutrasDespesas = self.outras_despesas,
                    )
                )

                session.commit()
                self.outras_despesas = 0

                print("Atualização concluída com sucesso.")
            except SQLAlchemyError as e:
                session.rollback()
                print("Erro ao atualizar o banco de dados:", str(e))
            # finally:
            #     session.close()

    def criar_pedido(self, e):
        # Clear existing data before processing new document
        self.datatable_itens_pedido.rows.clear()
        self.botao_criar.disabled = True

        # Show loading dialog
        loading = ft.AlertDialog(
            content=ft.Container(
                content=ft.ProgressRing(),
                alignment=ft.alignment.center,
            ),
            bgcolor=ft.colors.TRANSPARENT,
            modal=True,
            disabled=True,
        )
        self.page.open(loading)

        try:
            url = "http://iseletrica.ddns.com.br:8091/api/documentos/"
            
            payload = {
                "StatusNotaFiscalEletronica": "A",
                "CriaDocumentoProntoParaSerLiberado": False,
                "TipoDocumento": "F",
                "TipoPagamento": "0",
                "CodigoEmpresa": "4",
                "DataEmissao": data_formatada,
                "DataReferencia": data_formatada,
                "DataReferenciaPagamento": data_formatada,
                "IdentificadorOperacao": '00A00000CW',
                "IdentificadorPessoa": "00A0000001",
                "Itens": self.ler_nfe.itens,
                "Identificador": "00B002AXO0",
                "Numero": "",
                "Observacao": "Documento importado do XML da NF de entrada de fornecedor.",
            }

            token = self.new_token()

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            
            # Vamos imprimir o payload para debug
            # print("Payload sendo enviado:", payload)
            print(json.dumps(payload, indent=4))
            
            response = requests.post(url, json=payload, headers=headers)
            
            # Vamos tentar pegar mais detalhes do erro
            # print("Status code:", response.status_code)
            # print("Response headers:", response.headers)
            
            try:
                error_detail = response.json()
                print("Response body:", error_detail)
            except:
                print("Response text:", response.text)

            # Agora vamos verificar o status code antes de prosseguir
            if response.status_code != 200:
                raise Exception(f"Erro do servidor: {response.status_code} - {response.text}")
                
            data = response.json()

            if not data.get('Erros'):
                nr_pedido = data['ListaObjetos'][0]['Numero']
                id_pedido_de_venda = data['ListaObjetos'][0]['Identificador']
                
                valor_capa = self.atualizar_itens_pedidos(id_pedido_de_venda)
                self.atualizar_capa_pedidos(id_pedido_de_venda, valor_capa)
                
                self.open_dialogo(f"Pedido {nr_pedido} criado com sucesso!")
            else:
                causa_do_erro = data['Erros'][0]['ErrorMessage']
                self.open_dialogo(f"Pedido não foi criado! {causa_do_erro}")
        
        except Exception as e:
            self.open_dialogo(f"Erro ao processar pedido: {str(e)}")
            return None
        
        finally:
            self.page.close(loading)
            if 'payload' in locals():
                payload.clear()
            self.ler_nfe.itens.clear()
            self.datatable_itens_pedido.rows.clear()
            self.botao_criar.disabled = True
            self.page.update()

        return data

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # IDENTIFICANDO PEDIDO SELECIONADO - Order
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def change_select(self, e):
        e.control.selected = not e.control.selected
        e.control.update()

        if e.control.selected:
            if self.tb_tabela.current:
                selected_row = e.control  # Pega a linha selecionada diretamente do evento
                selected_cell_value = selected_row.cells[0].content.value
                # print(selected_cell_value)
                self.tb_tab_pedido.current.selected_index = 1
                self.tb_tab_pedido.current.update()
        else:
            print('Deselected')

    async def preenche_tabela(self):
        try:         
            # Limpe as linhas existentes, se necessário
            self.datatable_itens_pedido.rows.clear()


            # Configuração inicial da barra de progresso
            self.progress_bar.visible = True
            self.progress_bar.value = 0
            await self.page.update_async()
            # ---------------------------------------------------------------------------------------------------------------------------------------

            if type(self.dados_nfe_xml)!= dict:
                mensagem = f"Produto com código {self.dados_nfe_xml} não encontrado. \nOu o produto possui quantidade de caracteres menor que o XML\nOu provavelmente não está vinculado ao CNPJ deste fornecedor."
                self.open_dialogo(mensagem)
            else:

                total_produtos = len(self.dados_nfe_xml['produtos'].items())
                self.progress_bar.visible = True
                for i, (produto_id, produto) in enumerate(self.dados_nfe_xml['produtos'].items(), 1):
                    self.progress_bar.value = i / total_produtos
                    await self.page.update_async()
                    # Processar o produto aqui
                    await asyncio.sleep(0.1)  # Usar asyncio.sleep em vez de time.sleep 
             
                    # Crie uma nova linha com os dados do produto
                    nova_linha = ft.DataRow(
                        cells=[
                                ft.DataCell(ft.Text(produto['codigo'])),
                                ft.DataCell(ft.Text(produto['descricao'])),
                                ft.DataCell(ft.Text(self.formatar_numero(float(produto['quantidade'])))),
                                ft.DataCell(ft.Text(self.formatar_numero(float(produto['valor_unitario'])))),
                                ft.DataCell(ft.Text(self.formatar_numero(float(produto['valor_total'])))),

                                # Adicione mais células conforme necessário
                        ],
                        selected=False,
                        on_select_changed = self.change_select,
                    )

                    # Adicione a nova linha à tabela
                    self.datatable_itens_pedido.rows.append(nova_linha)

                self.progress_bar.visible = False
                # Finaliza a barra de progresso
                self.page.update()

                # Atualize a tabela para refletir as novas linhas
                self.datatable_itens_pedido.update()
                self.botao_criar.disabled=True
            
        except ValueError as e:
            print(e)
            
    # Função para lidar com o resultado da seleção de arquivos
    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            # Extrair caminhos dos arquivos
            file_paths = [file.path for file in e.files]  
            self.selected_files.value = "\n".join(file_paths)  # Exibir caminhos separados por linha
            self.selected_files.update()
            
            # Limpa tudo
            # -----------------------------------------------------------------------------------------
            # self.dados_nfe_xml.clear()

            # self.payload.clear()  # Reset payload

            # self.ler_nfe.itens.clear()  # Clear self.itens
            
            self.datatable_itens_pedido.rows.clear()
            # -----------------------------------------------------------------------------------------

            
            self.dados_nfe_xml = self.ler_nfe.ler_nfe(self.selected_files.value)
            # self.dados_nfe_xml = ler_nfe(self.selected_files.value)

            await self.preenche_tabela()
            self.botao_criar.disabled=False
            self.botao_criar.update()
            
        else:
            self.selected_files.value = "Cancelled!"
            self.selected_files.update()

    # Criação do FilePicker
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(col={"md": 12}, size=20, weight="bold")  # Estilo do texto exibido

    # Adicionando o FilePicker ao overlay da página
    # page.overlay.append(pick_files_dialog)

    def get_content(self):
        # Criação dos botões
        botao_importar = MyButton(
            text="Importar Pedido", 
            on_click=lambda _: self.pick_files_dialog.pick_files(
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["xml", "xmls"],                 
                allow_multiple=False
            )
        )

        self.botao_criar.disabled = True

        botoes_pedido = ft.Container(
            content=ft.Row(
                controls=[
                    botao_importar, 
                    self.botao_criar,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
            # bgcolor=ft.colors.SURFACE_VARIANT
        )

        # Tabela com itens
        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.colunas_itens)
        self.preenche_tabela_vazia(5)

        # Área de conteúdo principal
        content_area = ft.Column(
            controls=[
                self.selected_files,
                ft.Container(# Barra de progresso
                    content=ft.Row(
                        controls=[
                            self.progress_bar
                        ],
                        expand=True,
                    ),
                    padding=ft.padding.symmetric(horizontal=16),
                ),                
                ft.Container(
                    content=self.datatable_itens_pedido,
                    expand=True,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # Layout final
        return ft.Column(
            controls=[
                ft.Container(
                    content=content_area,
                    expand=True,
                ),
                botoes_pedido,
            ],
            spacing=0,
            expand=True,
        )

