import flet as ft
import requests
import json
# from partials.ler_nfe import *
# from partials.ler_nfe import LerNFE
from database.models import CodigoProduto

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

class BaseConnection:
    def __init__(self):
        self.client_id = "BimerAPI"
        self.client_secret = "0000d45dacfaa0c83913084d6f74c3a0"
        self.grant_type = "password"
        self.nonce = "123456789"
        self.username = None
        self.password = None
        self.datatable_itens_pedido = None

        self.progress_bar = ft.ProgressBar(
            width=None,  # Removemos o width fixo
            visible=False,
            value=0,
            expand=True
        )

        # self.ler_nfe = LerNFE()      

        self.loading = ft.AlertDialog(
            content=ft.Container(
                content=ft.ProgressRing(),
                alignment=ft.alignment.center,
            ),
            bgcolor=ft.colors.TRANSPARENT,
            modal=True,
            disabled=True,
        )

    def ler_cfg(self):
        """Lê as credenciais do arquivo JSON e atribui às variáveis da classe"""
        with open("cfg_api.json", "r") as f:
            data = json.load(f)
            # Acessar a lista de itens
            self.username = data.get("username")
            self.password = data.get("password_api")

    def get_params(self):
        self.ler_cfg()
        """Retorna os parâmetros necessários para autenticação"""
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': self.grant_type,
            'nonce': self.nonce,
            'username': self.username,
            'password': self.password
        }
        
    def new_token(self):
        """Obtém um novo token de acesso"""
        url = "http://iseletrica.ddns.com.br:8091/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        params = self.get_params()
        response = requests.post(url, headers=headers, data=params)

        if response.status_code != 200:
            raise Exception(f"Erro na solicitação do Token: {response.status_code}")

        data = json.loads(response.text)
        return data['access_token']
    
    def encontrar_cd_chamada_bimer(self, codigo_ean, codigo_fornecedor):
        # --000001 - 00A0000002 - PERSONALIZADO
        # --000003 - 00A0000004 - CODIGO EAN
        # --000004 - 00A0000005 - FORNECEDOR
        result_idproduto_ean = session.query(CodigoProduto).filter(CodigoProduto.IdTipoCodigoProduto == '00A0000004',
                                                                CodigoProduto.CdChamada == codigo_ean).all()
        
        result_idproduto_chamada = session.query(CodigoProduto).filter(CodigoProduto.IdTipoCodigoProduto == '00A0000005',
                                                                CodigoProduto.CdChamada == codigo_fornecedor).all()

        if len(result_idproduto_ean) >= 1:
            id_produto = [codigo.IdProduto.strip() for codigo in result_idproduto_ean]
        else:
            id_produto = [codigo.IdProduto.strip() for codigo in result_idproduto_chamada]

        # Verifica se a lista id_produto está vazia ou não
        if id_produto:
            # Se houver itens na lista, prossegue com a próxima etapa
            result_idproduto_principal = session.query(CodigoProduto).filter(
                CodigoProduto.IdTipoCodigoProduto == '00A0000002',
                CodigoProduto.IdProduto == id_produto[0],
                CodigoProduto.StCodigoPrincipal == 'S'
            ).all()
            
            if result_idproduto_principal:
                return result_idproduto_principal[0].CdChamada.strip()
            else:
                return None
        else:
            return None 

    def preenche_tabela_vazia(self, num_colunas=2):
        """
        Preenche uma tabela com um número variável de colunas.
        
        Args:
            num_colunas (int): Número total de colunas desejado (mínimo 2)
        """
        # Garante que o número de colunas seja pelo menos 2
        num_colunas = max(2, num_colunas)
        
        self.datatable_itens_pedido.rows.clear()
        
        # Cria a lista de células
        cells = [
            ft.DataCell(ft.Text('000000')),  # Primeira coluna fixa
            ft.DataCell(ft.Text('NENHUM ITEM A SER EXIBIDO.')),  # Segunda coluna fixa
        ]
        
        # Adiciona células extras com '0' conforme necessário
        cells.extend([ft.DataCell(ft.Text('0')) for _ in range(num_colunas - 2)])
        
        nova_linha = ft.DataRow(
            cells=cells,
            selected=False,
            on_select_changed=self.change_select,
        )
        
        # Adiciona a nova linha à tabela
        self.datatable_itens_pedido.rows.append(nova_linha)

    def open_dialogo(self, mensagem):
        self.dialogo.title = ft.Text(value="Atenção!")
        self.dialogo.content = ft.Text(value=mensagem)
        self.page.dialog = self.dialogo
        self.dialogo.open = True
        self.page.update()



    # ***** CRT significa *****
    # 1: Simples Nacional
    # 2: Simples Nacional - Excesso de Sublimite de Receita Bruta
    # 3: Regime Normal
    # 4: Microempreendedor Individual (MEI) - Novo código, implementado a partir de setembro de 2024
    def valida_crt(self, crt):
        match crt:
            case 1:
                # Código a ser executado se valor == padrão1
                return 'Simples Nacional'
            case 2:
                # Código a ser executado se valor == padrão2
                return 'Simples Nacional - Excesso de Sublimite de Receita Bruta'   
            case 3:
                # Código a ser executado se valor == padrão1
                return 'Normal'
            case 4:
                # Código a ser executado se valor == padrão1
                return 'Microempreendedor Individual (MEI)'             
            case _:
                # Código padrão, se nenhum caso anterior corresponder
                return 'Não se enquadra em nada!'
    
    def formatar_numero(self, valor):
        return locale.format_string('%.2f', valor, grouping=True)                