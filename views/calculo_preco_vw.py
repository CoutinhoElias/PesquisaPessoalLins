import flet as ft
from partials.all_imports import *
from reports.custo_rpt import RelatorioGerador
from partials.ler_nfe import *
import asyncio
from asyncio import sleep
import time  # Apenas para simular um processo

''' Criei uma classe chamada BaseConnection que será herdada pelas minhas classes
que usarem o super().__init__().
'''
class CalculoPrecoVW(BaseConnection):
    def __init__(self, page: ft.Page, app_instance):
        super().__init__()

        self.page = page
        self.tabela_ref = ft.Ref[ft.DataTable]()
        self.tabs_from_main = ft.Ref[ft.Tabs]
        self.fields_vl_frete = ft.Ref[ft.TextField]         

        self.dados_nfe_xml = None

        self.caminho_do_relatorio = None

        # self.ler_nfe = LerNFE()

        self.page.add(self.progress_bar)  # Adiciona a barra de progresso à página


        # Inicialização do FilePicker e texto para exibir arquivos selecionados
        self.selected_files = ft.Text()
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)

        self.outras_despesas = 0

        # Construção da TABELA
        # =============================================================================================================================
        # Definição do Ref().
        self.tb_tabela = ft.Ref[ft.DataTable]()
        self.tb_tabela_itens_pedido = ft.Ref[ft.DataTable]()
        self.tb_tab_pedido = ft.Ref[ft.Tab]()

        # =============================================================================================================================

        # LISTA DE ITENS DA TABELA
        self.colunas_itens = [
            ft.DataColumn(ft.Text("Código", width=47), on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Descricao", width=63), on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Unitário", width=55), numeric=True, on_sort=lambda e: sort_column(e)),
            # ft.DataColumn(ft.Text("I", width=.2), numeric=False, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Aliquota IPI", width=55), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Aliquota ICMS", width=55), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("IR/FAT", width=50), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Frete", width=40), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Custos", width=45), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("ML. Atual", width=45), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("ML. Esperado", width=60), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Finan.", width=45), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Preço Calculado", width=65), numeric=True, on_sort=lambda e: sort_column(e)),
            ft.DataColumn(ft.Text("Valor Sistema", width=60), numeric=True, on_sort=lambda e: sort_column(e)),
        ]

        self.datatable_itens_pedido = create_datatable(self.tb_tabela_itens_pedido, self.colunas_itens)
        self.table_order_items = my_table(self.datatable_itens_pedido)
        # =========================================================================================================================================

        self.botao_criar = MyButton(text="Imprimir", on_click=self.mostra_relatorio, bgcolor=ft.Colors.BLUE_300, expand=True)

        # Criação dos botões com expand=True para ocupar o espaço disponível
        self.botao_importar = MyButton(text="Importar XML", on_click=lambda _: self.pick_files_dialog.pick_files(
                                                                            file_type=ft.FilePickerFileType.CUSTOM,
                                                                            allowed_extensions=["xml", "xmls"],                 
                                                                            allow_multiple=False))

        # botao_criar = MyButton(text="Criar Pedido", on_click=self.criar_pedido, bgcolor=ft.Colors.BLUE_300, expand=True)
        self.botao_criar.disabled=True

        self.dados_emissor =  ft.Row(
            controls=[
                ft.Text("Nome Fornecedor: ", weight=ft.FontWeight.BOLD), ft.Text("cnpj"), ft.Text("Nome Fornecedor"),
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinhamento do Row
        )

        self.regime_emissor =  ft.Row(
            controls=[
                ft.Text("O Regime deste fornecedor é: ", weight=ft.FontWeight.BOLD), ft.Text("regime"),
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinhamento do Row
        )        

        self.regiao_emissor =  ft.Row(
            controls=[
                ft.Text("A região é: ", weight=ft.FontWeight.BOLD), ft.Text("Região"),
            ],
            alignment=ft.MainAxisAlignment.START,  # Alinhamento do Row
        ) 

        self.botoes_pedido =  ft.Row(
            controls=[
                self.botao_importar, self.botao_criar,
            ],
            alignment=ft.MainAxisAlignment.END,  # Alinhamento do Row
        )


        self.unificado = self.ler_nfe.unificado # self.verifica_existencia_configuracao() # Função no arquivo ler_xml_nfe.py
        self.norte, self.nordeste, self.ceara, self.centro_oeste, self.sudeste, self.sul = region_tile() 

        # Mesmo tipo dos TFs acima mas aqui com outro propósito.
        # ir_fat, margem_lucro_esperado, finan
        self.ir_fat = ft.TextField(
            label="IR/FAT", 
            hint_text="IR/FAT",
            col={"md": 2}, 
            # on_blur=lambda event: alteracao(event.control.value), 
            focused_border_color = ft.colors.GREEN,
            # input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.margem_lucro_esperado = ft.TextField(
            label="Margem de Lucro Esperado", 
            hint_text="Margem de Lucro Esperado",
            col={"md": 2}, 
            # on_blur=lambda event: alteracao(event.control.value), 
            focused_border_color = ft.colors.GREEN,
            # input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.finan = ft.TextField(
            label="Finan", 
            hint_text="Finan",
            col={"md": 2}, 
            # on_blur=lambda event: alteracao(event.control.value), 
            focused_border_color = ft.colors.GREEN,
            # input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.dados_custo = ft.ExpansionTile(
            title=ft.Text("Informações para custo", weight=ft.FontWeight.BOLD,),
            subtitle=ft.Text("Ajustes de cálculo de custo."),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            # initially_expanded=True,
            collapsed_text_color=ft.colors.RED,
            text_color=ft.colors.RED,
            controls_padding=5,
            # ref=??????????,
            # ir_fat, margem_lucro_esperado, finan
            controls=[
                ft.ListTile(title=ft.Text("Ajustes:")),
                ft.ResponsiveRow(
                    ref=fields_sul,
                    controls=                 
                    [
                        self.ir_fat, self.margem_lucro_esperado, self.finan
                    ],
                    run_spacing={"xs": 12},
                ),
            ],
        )

        self.ir_fat.value = self.unificado["custo"]["ir_fat"]
        self.margem_lucro_esperado.value = self.unificado["custo"]["margem_lucro_esperado"]
        self.finan.value = self.unificado["custo"]["finan"]

        # Preencher valores para cada região
        self.fill_region_values(self.norte, "Norte", self.unificado)
        self.fill_region_values(self.nordeste, "Nordeste", self.unificado)
        self.fill_region_values(self.ceara, "Ceará", self.unificado)
        self.fill_region_values(self.centro_oeste, "Centro-Oeste", self.unificado)
        self.fill_region_values(self.sudeste, "Sudeste", self.unificado)
        self.fill_region_values(self.sul, "Sul", self.unificado) 

        # Regiões:
        # tabs_from_main.current.tabs[1].content.content.controls[0]
        # 0 = norte
        # 1 = nordeste
        # 2 = ceara
        # 3 = centro_oeste
        # 4 = sudeste
        # 5 = sul

        self.floating_action_button = ft.Container(
            content=ft.FloatingActionButton(
                icon=ft.icons.SAVE_OUTLINED, 
                bgcolor=ft.colors.GREEN,
                tooltip='Salva Configurações.',
                on_click=self.salva_valores_configuracao, 
            ),
            alignment=ft.Alignment(x=1, y=-1)
        )

    def salva_valores_configuracao(self, e):
        unificado_alteracao = {
                    "regioes_estados": {
                        "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
                        "Nordeste": ["ES", "AL", "BA", "MA", "PB", "PE", "PI", "RN", "SE"],
                        "Ceará": ["CE"],
                        "Centro-Oeste": ["DF", "GO", "MT", "MS"],
                        "Sudeste": ["MG", "RJ", "SP"],                        
                        "Sul": ["PR", "RS", "SC"]
                    },
                    "fatores": {
                        'default': {
                            'Norte': {
                                    #tabs_from_main.current.tabs[TAB].content.content.controls[REGIAO].controls[ELETRICO1, INFORMATICA3].controls[SIMPLES0, IMPORTADO1, PADRAO2].value
                                '1': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[1].controls[0].value,
                                '2': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[1].controls[0].value,
                                'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[1].controls[1].value, 
                                            '12': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[1].controls[2].value}
                            },
                            'Nordeste': {
                                '1': self.tabs_from_main.current.tabs[1].content.content.controls[1].controls[1].controls[0].value,
                                '2': self.tabs_from_main.current.tabs[1].content.content.controls[1].controls[1].controls[0].value,
                                'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[1].controls[1].controls[1].value, 
                                            '12': self.tabs_from_main.current.tabs[1].content.content.controls[1].controls[1].controls[2].value}
                            },
                            'Ceará': {
                                '1': self.tabs_from_main.current.tabs[1].content.content.controls[2].controls[1].controls[0].value,
                                '2': self.tabs_from_main.current.tabs[1].content.content.controls[2].controls[1].controls[0].value,
                                'default': self.tabs_from_main.current.tabs[1].content.content.controls[2].controls[1].controls[2].value, 
                            },
                            'Centro-Oeste': {
                                '1': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[1].controls[0].value,
                                '2': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[1].controls[0].value,
                                'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[1].controls[1].value, 
                                            '12': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[1].controls[2].value}
                            },
                            'Sudeste': {
                                '1': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[1].controls[0].value,
                                '2': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[1].controls[0].value,
                                'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[1].controls[1].value, 
                                            'default': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[1].controls[2].value}
                            },
                            'Sul': {
                                '1': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[1].controls[0].value,
                                '2': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[1].controls[0].value,
                                'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[1].controls[1].value, 
                                            'default': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[1].controls[2].value}
                            },
                        }
                    },
                    "fatores_informatica": {
                        'Norte': {
                                #tabs_from_main.current.tabs[TAB].content.content.controls[REGIAO].controls[ELETRICO1, INFORMATICA3].controls[SIMPLES0, IMPORTADO1, PADRAO2].value
                            '1': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[3].controls[0].value,
                            '2': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[3].controls[0].value,
                            'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[3].controls[1].value, 
                                        '12': self.tabs_from_main.current.tabs[1].content.content.controls[0].controls[3].controls[2].value}
                        },
                        'Nordeste': {
                            '1': self.tabs_from_main.current.tabs[1].content.content.controls[1].controls[3].controls[0].value,
                            '2': self.tabs_from_main.current.tabs[1].content.content.controls[1].controls[3].controls[0].value,
                            'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[1].controls[1].value, 
                                        '12': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[1].controls[2].value}
                        },
                        'Ceará': {
                            '1': self.tabs_from_main.current.tabs[1].content.content.controls[2].controls[3].controls[0].value,
                            '2': self.tabs_from_main.current.tabs[1].content.content.controls[2].controls[3].controls[0].value,
                            'default': self.tabs_from_main.current.tabs[1].content.content.controls[2].controls[3].controls[2].value, 
                        },
                        'Centro-Oeste': {
                            '1': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[3].controls[0].value,
                            '2': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[3].controls[0].value,
                            'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[3].controls[1].value, 
                                        '12': self.tabs_from_main.current.tabs[1].content.content.controls[3].controls[3].controls[2].value}
                        },
                        'Sudeste': {
                            '1': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[3].controls[0].value,
                            '2': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[3].controls[0].value,
                            'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[3].controls[1].value, 
                                        'default': self.tabs_from_main.current.tabs[1].content.content.controls[4].controls[3].controls[2].value}
                        },
                        'Sul': {
                            '1': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[3].controls[0].value,
                            '2': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[3].controls[0].value,
                            'default': {'4': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[3].controls[1].value, 
                                        'default': self.tabs_from_main.current.tabs[1].content.content.controls[5].controls[3].controls[2].value}
                        },
                    },
                    "custo": {
                        'ir_fat': self.tabs_from_main.current.tabs[1].content.content.controls[7].controls[1].controls[0].value,
                        'margem_lucro_esperado': self.tabs_from_main.current.tabs[1].content.content.controls[7].controls[1].controls[1].value,
                        'finan': self.tabs_from_main.current.tabs[1].content.content.controls[7].controls[1].controls[2].value,                      
                    }
                }

        with open('\\\\server_erp\\alterdat\\db\\unificado.json', 'w', encoding='utf-8') as file:
            json.dump(unificado_alteracao, file, ensure_ascii=False, indent=4)      

        self.open_dialogo("Dados Salvos!")

    def on_text_change(self, e):
        # Verifica se há uma vírgula no texto e a substitui por um ponto
        if "," in e.control.value:
            e.control.value = e.control.value.replace(",", ".")
            e.control.update()

    def fill_region_values(self, expansion_tile, region_name, unificado):
        if region_name not in('Ceará', 'Sudeste', 'Sul'):
            # Elétricos
            expansion_tile.controls[1].controls[0].value = unificado["fatores"]["default"][region_name]["1"]
            expansion_tile.controls[1].controls[1].value = unificado["fatores"]["default"][region_name]["default"]["4"]
            expansion_tile.controls[1].controls[2].value = unificado["fatores"]["default"][region_name]["default"]["12"]
            
            # Informática
            expansion_tile.controls[3].controls[0].value = unificado["fatores_informatica"][region_name]["1"]
            expansion_tile.controls[3].controls[1].value = unificado["fatores_informatica"][region_name]["default"]["4"]
            expansion_tile.controls[3].controls[2].value = unificado["fatores_informatica"][region_name]["default"]["12"]
        elif region_name == 'Ceará':
            expansion_tile.controls[1].controls[0].value = unificado["fatores"]["default"][region_name]["1"]
            expansion_tile.controls[1].controls[1].value = unificado["fatores"]["default"][region_name]["default"]
            expansion_tile.controls[1].controls[2].value = unificado["fatores"]["default"][region_name]["default"]
            
            # Informática
            expansion_tile.controls[3].controls[0].value = unificado["fatores_informatica"][region_name]["1"]
            expansion_tile.controls[3].controls[1].value = unificado["fatores_informatica"][region_name]["default"]
            expansion_tile.controls[3].controls[2].value = unificado["fatores_informatica"][region_name]["default"]
        else:
            # Elétricos
            expansion_tile.controls[1].controls[0].value = unificado["fatores"]["default"][region_name]["1"]
            expansion_tile.controls[1].controls[1].value = unificado["fatores"]["default"][region_name]["default"]["4"]
            expansion_tile.controls[1].controls[2].value = unificado["fatores"]["default"][region_name]["default"]["default"]
            
            # Informática
            expansion_tile.controls[3].controls[0].value = unificado["fatores_informatica"][region_name]["1"]
            expansion_tile.controls[3].controls[1].value = unificado["fatores_informatica"][region_name]["default"]["4"]
            expansion_tile.controls[3].controls[2].value = unificado["fatores_informatica"][region_name]["default"]["default"]
        
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
                self.dados_emissor.controls[1].value = self.dados_nfe_xml['emissor']['cnpj']
                self.dados_emissor.controls[2].value = self.dados_nfe_xml['emissor']['nome']
                self.dados_emissor.update()

                self.regime_emissor.controls[1].value = self.valida_crt(int(self.dados_nfe_xml['emissor']['crt']))
                self.regime_emissor.update()

                self.regiao_emissor.controls[1].value = self.dados_nfe_xml['emissor']['regiao']
                self.regiao_emissor.update()

                valor_produtos = float(self.dados_nfe_xml['totais']['valor_produtos'])
                frete_nota = float(self.dados_nfe_xml['totais']['frete'])

                frete_nota_manual = self.dados_nfe_xml['totais']['frete_manual']
                media_frete_calculado = (frete_nota + frete_nota_manual) / valor_produtos
                # for produto in self.dados_nfe_xml['produtos']
                # Itera sobre cada produto no dicionário
                for produto_id, produto in self.dados_nfe_xml['produtos'].items():
                    # Atualiza o valor de MediaFreteCalculado
                    produto['MediaFreteCalculado'] =  media_frete_calculado # .replace(',','.')

                # print(json.dumps(self.dados_nfe_xml, indent=4))

                total_produtos = len(self.dados_nfe_xml['produtos'].items())
                linhas = []
                self.progress_bar.visible = True

                # Fecha a animação para iniciar outra de progresso.
                self.page.close(self.loading)
                self.page.update()

                for i, (produto_id, produto) in enumerate(self.dados_nfe_xml['produtos'].items(), 1):
                    self.progress_bar.value = i / total_produtos
                    await self.page.update_async()
                    # Processar o produto aqui
                    await asyncio.sleep(0.1)  # Usar asyncio.sleep em vez de time.sleep 
                      

                    # Crie uma nova linha com os dados do produto
                    p_ipi = produto['impostos'].get('IPI', {}).get('pIPI', '0.00')

                    preco_calculado = float(produto['PrecoVendaCalculado'])
                    preco_anterior = float(produto['PrecoVendaAnterior'])

                    # self.page.update()
                    nova_linha_datatable = ft.DataRow(
                        cells=[
                                ft.DataCell(ft.Text(produto['codigo'])),
                                ft.DataCell(ft.Text(produto['descricao'])),                                
                                ft.DataCell(ft.Text("{:.2f}".format(float(produto['valor_unitario'])))),
                                # ft.DataCell(ft.Text(produto['i'])),
                                ft.DataCell(ft.Text("{:.2f}".format(float(p_ipi)), text_align="right")),
                                ft.DataCell(ft.Text(produto['impostos'].get('ICMS', {}).get('aliquota_calculada', '0.00'), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(float(self.ir_fat.value)), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(float(produto['MediaFreteCalculado'])*100), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(produto['Custos']), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(produto['MargemLucroAtual']), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(produto['MargemLucroEsperado']), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(produto['Finan']), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(produto['PrecoVendaCalculado']), text_align="right")),
                                ft.DataCell(ft.Text("{:.2f}".format(produto['PrecoVendaAnterior']), text_align="right"))
                        ],
                        selected=False,
                        on_select_changed = self.change_select,
                    )

                    # Lista criada para alimentar a tabela no relatório PDF ReportLab.
                    linhas.append([produto['codigo'], 
                                  produto['descricao'][:50], 
                                  self.formatar_numero(float(produto['valor_unitario'])),
                                  self.formatar_numero(float(p_ipi)) + "%",
                                  self.formatar_numero(float(produto['impostos'].get('ICMS', {}).get('aliquota_calculada', '0.00'))) + "%",
                                  self.formatar_numero(float(self.ir_fat.value)) + "%",
                                  self.formatar_numero(float(produto['MediaFreteCalculado'])*100) + "%",
                                  self.formatar_numero(float(produto['Custos'])) + "%",
                                  self.formatar_numero(produto['MargemLucroAtual']) + "%",
                                  self.formatar_numero(produto['MargemLucroEsperado']) + "%",
                                  self.formatar_numero(produto['Finan']) + "%",
                                  self.formatar_numero(produto['PrecoVendaCalculado']),
                                  self.formatar_numero(produto['PrecoVendaAnterior'])
                                ]
                            )                
                    
                    # Adicione a nova linha à tabela
                    self.datatable_itens_pedido.rows.append(nova_linha_datatable)

                    # Cabeçalho das colunas da tabela no ReportLab.
                    cabecalho = ["Código", "Descrição", "Valor\nUnitário", "Alíquota\nIPI", "Alíquota\nICMS", "IR/FAT", "Frete", "Custos", "M. Lucro\nAtual", "M. Lucro\nEsperado", "Finan.", "Preço\nCalculado", "Valor\nSistema"]
                
                self.progress_bar.visible = False
                # Finaliza a barra de progresso
                self.page.update()

                # Gera arquivo com relatório só esperando ser aberto.
                # self.gerar_relatorio_pdf(cabecalho, linhas)
                self.gerador.gerar_relatorio_pdf(
                    cabecalho_itens=cabecalho,
                    linhas_itens=linhas,
                    nome_arquivo="relatorio_custo.pdf"
                )
            

        except ValueError as e:
            print(e)

    def mostra_relatorio(self, e):

        caminho_absoluto = os.path.abspath('relatorio_custo.pdf')
        self.caminho_do_relatorio = caminho_absoluto

        # print(self.caminho_do_relatorio)      

        # Verifica o sistema operacional e abre o PDF
        if platform.system() == "Windows":
            os.startfile(self.caminho_do_relatorio)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", self.caminho_do_relatorio])
        else:  # Linux
            subprocess.Popen(["xdg-open", self.caminho_do_relatorio])        

    def recalcula_custos(self):
        # Cálculo de Custos
        fretes = ((float(self.dados_nfe_xml['totais']['frete']) + float(self.dados_nfe_xml['totais']['frete_manual'])) / float(self.dados_nfe_xml['totais']['valor_produtos'])) * 100

        print(json.dumps(self.dados_nfe_xml, indent=4))

        for produto_id, produto in self.dados_nfe_xml['produtos'].items():
            # Atualiza no dicionário geral
            self.dados_nfe_xml['Custos'] = (float(produto['impostos']['IPI']['pIPI']) + 
                    float(produto['impostos']['ICMS']['aliquota_calculada']) + 
                    float(self.dados_nfe_xml['totais']['ir_fat']) + 
                    float(fretes) + 100)  # 100 pode ser transformado em percentual aqui
            # Também no dicionário local
            produto['Custos'] = self.dados_nfe_xml['Custos']

            # ---------------------------------------------------------------------------------------------------

            # Atualiza no dicionário geral
            self.dados_nfe_xml['PrecoVendaCalculado'] = (float(produto['valor_unitario']) * (float(self.dados_nfe_xml['Custos'])/100) * (float(self.unificado["custo"]["margem_lucro_esperado"])/100) * (float(self.unificado["custo"]["finan"])/100))
            # Também no dicionário local
            produto['PrecoVendaCalculado'] = self.dados_nfe_xml['PrecoVendaCalculado']
            
            # ---------------------------------------------------------------------------------------------------
            # Atualiza no dicionário geral
            self.dados_nfe_xml['MargemLucroAtual'] = float(produto['PrecoVendaAnterior'] * 100) / (float(produto['valor_unitario']) * (float(self.dados_nfe_xml['Custos'])/100) * (float(self.unificado["custo"]["ir_fat"])/100))
            # Também no dicionário local
            produto['MargemLucroAtual'] = float(produto['PrecoVendaAnterior'] * 100) / (float(produto['valor_unitario']) * (float(self.dados_nfe_xml['Custos'])/100) * (float(self.unificado["custo"]["ir_fat"])/100))

            print(f'Custos: {self.dados_nfe_xml['Custos']}\nPrecoVendaCalculado: {self.dados_nfe_xml['PrecoVendaCalculado']}\nMargemLucroAtual: {self.dados_nfe_xml['MargemLucroAtual']}')


        # Exibindo o dicionário atualizado
        print(json.dumps(self.dados_nfe_xml, indent=4))

    async def frete_manual_async(self):
        done = asyncio.Event()  # Evento para esperar a entrada do usuário

        # Cria o TextField e armazena a referência
        frete_field = ft.TextField(label="Digite o valor do Frete", on_blur=self.on_text_change)

        def salvar(e):
            # Acessa o valor do TextField diretamente
            try:
                self.dados_nfe_xml['totais']['frete_manual'] = float(frete_field.value)
                
                self.recalcula_custos()

                self.page.dialog.open = False  # Fecha o diálogo                
                done.set()  # Libera o evento
                self.page.update()
            except ValueError:
                # Trate o caso em que a conversão para float falha
                self.open_dialogo("Por favor, insira um valor numérico válido.")
                self.page.update()

        def cancelar(e):
            self.page.dialog.open = False  # Fecha o diálogo
            done.set()  # Libera o evento
            self.page.update()

        botao_salvar = MyButton(text="Salvar", on_click=salvar, bgcolor=ft.Colors.RED, expand=True)
        botao_cancelar = MyButton(text="Cancelar", on_click=cancelar, bgcolor=ft.Colors.BLUE_300, expand=True)

        # Configura o modal
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Esta nota possui conhecimento de transporte?"),
            content=frete_field,  # Usa a referência do TextField
            actions=[
                botao_salvar,
                botao_cancelar,
            ],
        )
        self.page.dialog.open = True
        self.page.update()

        await done.wait()  # Aguarda o evento ser liberado

    async def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            # Extrair caminhos dos arquivos
            file_paths = [file.path for file in e.files]  
            self.selected_files.value = "\n".join(file_paths)  # Exibir caminhos separados por linha
            self.selected_files.update()
            
            # Abre a animação de tela para acalmar o coração do usuário.
            sleep(3)
            self.page.open(self.loading) 
            self.page.update()           

            # Lê os dados da NFE
            self.dados_nfe_xml = self.ler_nfe.ler_nfe(self.selected_files.value)
            self.gerador = RelatorioGerador(self.dados_nfe_xml)
            
            # Preenche a tabela
            frete_nota = float(self.dados_nfe_xml['totais']['frete'])
            if frete_nota <= 0:
                print("Neste momento não tem frete no XML")
                
                # Chama o modal e espera o resultado
                await self.frete_manual_async()

                frete_manual = self.dados_nfe_xml['totais'].get('frete_manual', 0)
                print(f"Frete manual registrado: {frete_manual}")
                # print(json.dumps(self.dados_nfe_xml, indent=4))

            await self.preenche_tabela()
            self.botao_criar.disabled = False
            self.botao_criar.update()
        else:
            self.selected_files.value = "Cancelled!"
            self.selected_files.update()

    # Criação do FilePicker
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text(col={"md": 12}, size=30, weight="bold")  # Estilo do texto exibido


    def get_content(self):
        divisor = ft.Divider(thickness=2, color=ft.colors.YELLOW)
        my_tab = ft.Tabs(
            ref=self.tabs_from_main,
            tabs=[
                ft.Tab(
                    text='Dados',
                    icon=ft.icons.TABLE_ROWS_OUTLINED,
                    content=ft.Container(
                        expand=True,
                        padding=ft.padding.all(2),
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    expand=True,  # Permite que a coluna expanda
                                    controls=[
                                        self.dados_emissor,
                                        self.regime_emissor,
                                        self.regiao_emissor,
                                        self.selected_files,
                                        ft.Container( # Barra de progresso
                                            content=ft.Row(
                                                controls=[
                                                    self.progress_bar
                                                ],
                                                expand=True,
                                            ),
                                            padding=ft.padding.symmetric(horizontal=16),
                                        ),
                                        ft.Container(
                                            height=540,  # Ajuste esta altura conforme necessário
                                            content=ft.Column(
                                                scroll=ft.ScrollMode.ALWAYS,
                                                controls=[self.datatable_itens_pedido]
                                            )
                                        ),
                                    ]
                                ),
                                self.botoes_pedido,  # Agora os botões ficarão fixos na parte inferior
                            ]
                        ),
                        alignment=ft.alignment.top_left,
                    )
                ),

                ft.Tab(
                    text='Parâmetros',
                    icon=ft.icons.SETTINGS,
                    content=ft.Container(
                        expand=False,
                        padding=ft.padding.all(2),
                        content=ft.Column(
                            expand=True,
                            controls=[
                                self.norte, self.nordeste, self.ceara,
                                self.centro_oeste, self.sudeste, self.sul,
                                divisor,
                                self.dados_custo,
                                self.floating_action_button,
                            ],
                            scroll=ft.ScrollMode.ALWAYS,  # Define a existência de um Scroll
                            on_scroll_interval=0,  # Define o intervalo de exibição
                        ),
                    ),
                ),
            ],
            selected_index=0,
            indicator_tab_size=True,
            label_color=ft.colors.GREEN,
            height=790,
        )

        # Adiciona uma linha padrão ao DataTable
        self.preenche_tabela_vazia(13)

        layout_final = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    my_tab,
                ]
            ),
        )
        return layout_final
