from sqlalchemy import create_engine, case, select, null
from sqlalchemy.orm import sessionmaker
from database.models import CodigoProduto, Produto, vwProdutoFornecedor, vwProdutoEmpresaPreco, Pessoa, PessoaCategoria  # Importa a classe CodigoProduto do módulo database.models
# from partials.all_imports import connection_string
from configs.settings import Criptografia
import pandas as pd
import logging

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class BuscaCodigoProduto:
    def __init__(self, cd_produto, cpf_cnpj):
        """Inicializa a classe com os parâmetros fornecidos e cria a engine e sessão do SQLAlchemy"""
        # CRIPTOGRAFA
        # 0 - Instancio a classe de criptografar senhas
        self.criptografia = Criptografia()
        # 1 - Chamo a função de criação da chave
        self.criptografia.init_criptografia()
        connection_string = self.criptografia.get_senha_descriptografada()

        self.engine = create_engine(connection_string)  # Cria a engine de conexão com o banco de dados
        self.Session = sessionmaker(bind=self.engine)  # Cria uma fábrica de sessões

        self.cd_produto = cd_produto
        self.cpf_cnpj = cpf_cnpj

        self.criptografia = Criptografia()

    def create_session(self):
        """Cria e retorna uma nova sessão"""
        return self.Session()

    def as_dict(self):
        return {
            'IdProduto': self.IdProduto,
            'CdChamada': self.CdChamada,
            'StCodigoPrincipal': self.StCodigoPrincipal,
            'IdTipoCodigoProduto': self.IdTipoCodigoProduto,
            'NomeProduto': self.NomeProduto
        }

    def get_all_produtos(self):
        """Obtém todos os produtos do banco de dados"""
        session = self.create_session()
        try:
            produtos = session.query(CodigoProduto).all()  # Consulta todos os produtos
            return produtos
        except Exception as e:
            print(f'Erro ao obter produtos: {e}')
            return []
        finally:
            session.close()  # Fecha a sessão

    def _get_price(self, id_produto, cd_empresa, id_preco):
        session = self.create_session()
        # Seleciona apenas a coluna VlPreco
        preco = session.query(vwProdutoEmpresaPreco).with_entities(vwProdutoEmpresaPreco.VlPreco).filter(
                    vwProdutoEmpresaPreco.IdProduto == id_produto, 
                    vwProdutoEmpresaPreco.IdPreco == id_preco,
                    vwProdutoEmpresaPreco.CdEmpresa == cd_empresa
                ).limit(1).scalar()  # Retorna um único valor

        # print(str(preco))

        return preco if preco is not None else 0  # Retorna 0 se preco for None
    
    def _set_price(self, id_produto, cd_empresa, id_preco):
        session = self.create_session()
        # Seleciona apenas a coluna VlPreco
        preco = session.query(vwProdutoEmpresaPreco).with_entities(vwProdutoEmpresaPreco.VlPreco).filter(
                    vwProdutoEmpresaPreco.IdProduto == id_produto, 
                    vwProdutoEmpresaPreco.IdPreco == id_preco,
                    vwProdutoEmpresaPreco.CdEmpresa == cd_empresa
                ).limit(1).scalar()  # Retorna um único valor

        # print(str(preco))



    def get_all_produtos_filtered(self):
        # logging.basicConfig()
        # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        # print(f'Produto atual {self.cd_produto}')
        """Obtém todos os produtos filtrados por código de chamada e retorna como um dicionário"""
        session = self.create_session()

        try:

        # Dicionário para consolidar os dados
            produto_dict = {
                'CdProdutoFornecedor': None,
                'CodigoProdutoBimer': None,
                'IdProduto': None,
                'NmProduto': None,
                'IdUnidade': None,
                'IdClassificacaoFiscal': None,
                'IdFornecedor': None,
                'CdFornecedor': None,
                'NmFornecedor': None,
                'CpfCgcFornecedor': None,
                'PrecoVendaCalculado': 0,
                'PrecoVendaAnterior': 0,
            }  

            # Primeira consulta traz somente o código do fornecedor
            produtos_query_1 = session.query(
                CodigoProduto.CdChamada,
                CodigoProduto.IdProduto,
                CodigoProduto.IdTipoCodigoProduto,
                Produto.NmProduto,
                Produto.IdUnidade,
                Produto.IdClassificacaoFiscal,
                vwProdutoFornecedor.IdPessoa,
                vwProdutoFornecedor.CdChamada.label('CodigoFornecedor'),
                vwProdutoFornecedor.NmPessoa,
                Pessoa.CdCPF_CGC,
            ).distinct() \
            .join(vwProdutoFornecedor, CodigoProduto.IdProduto == vwProdutoFornecedor.IdProduto) \
            .join(Produto, CodigoProduto.IdProduto == Produto.IdProduto) \
            .join(Pessoa, vwProdutoFornecedor.IdPessoa == Pessoa.IdPessoa) \
            .join(PessoaCategoria, Pessoa.IdPessoa == PessoaCategoria.IdPessoa) \
            .filter(
                CodigoProduto.CdChamada == self.cd_produto,
                CodigoProduto.IdTipoCodigoProduto.in_(['00A0000005', '00A0000002']),
                Produto.TpProduto.in_(['C', 'R']),
                Pessoa.CdCPF_CGC == self.cpf_cnpj,
                PessoaCategoria.IdCategoria == '0000000006'
            )

            id_produto = [produto.IdProduto for produto in produtos_query_1]
            cd_produto_fornecedor = [produto.CdChamada for produto in produtos_query_1]

            # Verifico se encontro o código do fornecedor
            if len(cd_produto_fornecedor)>0:
                produto_dict['CdProdutoFornecedor'] = cd_produto_fornecedor[0].strip()
            else:
                produto_dict['CdProdutoFornecedor'] = f'erro - {self.cd_produto}'

            # print(str(produtos_query_1))

            if len(id_produto)==0:
                id_produto=['1']

            # Segunda consulta
            produtos_query_2 = session.query(
                CodigoProduto.CdChamada,
                CodigoProduto.IdProduto,
                CodigoProduto.IdTipoCodigoProduto,
                Produto.NmProduto,
                Produto.IdUnidade,
                Produto.IdClassificacaoFiscal,
            ).distinct() \
            .join(Produto, CodigoProduto.IdProduto == Produto.IdProduto) \
            .filter(
                CodigoProduto.IdProduto == id_produto[0],
                CodigoProduto.IdTipoCodigoProduto.in_(['00A0000005', '00A0000002']),
                CodigoProduto.StCodigoPrincipal == 'S',
                Produto.TpProduto.in_(['C', 'R']),
            )

            # print(str(produtos_query_2))

            cd_produto_bimer = [produto_query_2.CdChamada for produto_query_2 in produtos_query_2]
            if len(cd_produto_bimer)>0:
                produto_dict['CodigoProdutoBimer'] = cd_produto_bimer[0].strip()
            else:
                produto_dict['CodigoProdutoBimer'] = f'erro - {self.cd_produto}'

            if not produtos_query_1:
                print("Produto não encontrado para o código e fornecedor fornecidos.")
                return []

            for produto_query_1 in produtos_query_1:
                # print(produto_query_1)

                print(produto_query_1.IdProduto.strip(), self._get_price(produto_query_1.IdProduto.strip(), 1, '00A0000002'))
                # Preenche os demais campos apenas uma vez
                produto_dict.update({
                    'IdProduto': produto_query_1.IdProduto.strip(),
                    'NmProduto': produto_query_1.NmProduto.strip(),
                    'IdUnidade': produto_query_1.IdUnidade.strip(),
                    'IdClassificacaoFiscal': produto_query_1.IdClassificacaoFiscal.strip(),
                    'IdFornecedor': produto_query_1.IdPessoa.strip(),
                    'CdFornecedor': produto_query_1.CodigoFornecedor.strip(),
                    'NmFornecedor': produto_query_1.NmPessoa,
                    'CpfCgcFornecedor': produto_query_1.CdCPF_CGC.strip(),
                    'PrecoVendaAnterior': self._get_price(produto_query_1.IdProduto, 1, '00A0000002')
                })
                # produto_dict.update({
                #     'IdProduto': produto_query_1.IdProduto.strip() if produto_query_1.IdProduto else '1',
                #     'NmProduto': produto_query_1.NmProduto.strip() if produto_query_1.NmProduto else 'ESTE PRODUTO NÃO FOI ENCONTRADO - DESCUBRA!',
                #     'IdUnidade': produto_query_1.IdUnidade.strip() if produto_query_1.IdUnidade else 'UN',
                #     'IdClassificacaoFiscal': produto_query_1.IdClassificacaoFiscal.strip() if produto_query_1.IdClassificacaoFiscal else '1',
                #     'IdFornecedor': produto_query_1.IdPessoa.strip() if produto_query_1.IdPessoa else '1',
                #     'CdFornecedor': produto_query_1.CodigoFornecedor.strip() if produto_query_1.CodigoFornecedor else '1',
                #     'NmFornecedor': produto_query_1.NmPessoa if produto_query_1.NmPessoa else '1',
                #     'CpfCgcFornecedor': produto_query_1.CdCPF_CGC.strip() if produto_query_1.CdCPF_CGC else '1',
                #     'PrecoVendaAnterior': self._get_price(produto_query_1.IdProduto, 1, '00A0000002') or 0.0
                # })
            return produto_dict
        except Exception as e:
            print(f'Erro ao obter produtos filtrados: {e}')
            return []
        finally:
            session.close()  # Fecha a sessão
