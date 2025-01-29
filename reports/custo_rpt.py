from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

class RelatorioGerador:
    def __init__(self, dados_nfe_xml):
        self.dados_nfe_xml = dados_nfe_xml
        self.caminho_do_relatorio = None
        self.margens = {
            'superior': 20,
            'inferior': 30,
            'esquerda': 30,
            'direita': 30
        }
        self.larguras_colunas = [40, 250, 44.54, 44.54, 44.54, 39.54, 44.54, 
                                49.54, 49.54, 49.54, 39.54, 64.54, 54.54]
        self.estilo_texto = self._criar_estilo_texto()

    def _criar_estilo_texto(self):
        """Cria e retorna o estilo de texto padrão."""
        styles = getSampleStyleSheet()
        estilo_texto = styles["Normal"]
        estilo_texto.alignment = 0  # Alinhado à esquerda
        return estilo_texto

    def _criar_documento(self, nome_arquivo):
        """Cria e retorna o objeto documento PDF."""
        return SimpleDocTemplate(
            nome_arquivo,
            pagesize=landscape(A4),
            leftMargin=self.margens['esquerda'],
            rightMargin=self.margens['direita'],
            topMargin=self.margens['superior'],
            bottomMargin=self.margens['inferior']
        )

    def _criar_tabela_itens(self, cabecalho_itens, linhas_itens):
        """Cria e estiliza a tabela principal de itens."""
        data = [cabecalho_itens] + linhas_itens
        tabela = Table(data, colWidths=self.larguras_colunas)
        
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (2, 1), (12, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
        ])
        tabela.setStyle(estilo)
        return tabela

    def _criar_info_cabecalho(self):
        """Cria as informações do cabeçalho."""
        emissor = self.dados_nfe_xml['emissor']
        return {
            'fornecedor': emissor['nome'],
            'data': datetime.now().strftime('%d/%m/%Y'),
            'cnpj': emissor['cnpj'],
            'regiao': emissor['regiao'],
            'empresa_tipo': self.valida_crt(int(emissor['crt'])),
            'numero_nota': self.dados_nfe_xml['numero_nota']
        }

    def _criar_tabela_cabecalho(self, nome_arquivo):
        """Cria e estiliza a tabela de cabeçalho."""
        info = self._criar_info_cabecalho()
        caminho_completo = os.path.abspath(nome_arquivo)
        
        info_cabecalho = [
            [
                Paragraph(f"Fornecedor: {info['cnpj']} - {info['fornecedor']}", self.estilo_texto),
                *[""] * 10,
                Paragraph(f"Data: {info['data']}", self.estilo_texto)
            ],
            [
                Paragraph(
                    f"Número da Nota: {info['numero_nota']} / Região: {info['regiao']} / "
                    f"Regime: {info['empresa_tipo']}", 
                    self.estilo_texto
                ),
                *[""] * 11
            ],
            [
                Paragraph(f"Caminho do arquivo: {caminho_completo}", self.estilo_texto),
                *[""] * 11
            ]
        ]

        tabela = Table(info_cabecalho, colWidths=[400] + [31.5] * 10 + [100])
        tabela.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (-1, 0), (-1, 0), 'RIGHT'),
            ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        return tabela

    def valida_crt(self, crt):
        """Valida e retorna o tipo de regime tributário."""
        regimes = {
            1: "Simples Nacional",
            2: "Simples Nacional - excesso",
            3: "Regime Normal"
        }
        return regimes.get(crt, "Regime não identificado")

    def gerar_relatorio_pdf(self, cabecalho_itens, linhas_itens, nome_arquivo="relatorio_custo.pdf"):
        """Gera o relatório PDF completo."""
        doc = self._criar_documento(nome_arquivo)
        
        tabela_cabecalho = self._criar_tabela_cabecalho(nome_arquivo)
        tabela_itens = self._criar_tabela_itens(cabecalho_itens, linhas_itens)
        
        elementos = [
            tabela_cabecalho,
            Spacer(1, 12),
            tabela_itens
        ]
        
        doc.build(elementos)
        self.caminho_do_relatorio = os.path.abspath(nome_arquivo)
        print(f"Relatório gerado em: {self.caminho_do_relatorio}")


        """
        O comando SPAN permite combinar células adjacentes em uma tabela, similar ao "merge cells" em planilhas. A sintaxe é:
        ('SPAN', (coluna_inicial, linha_inicial), (coluna_final, linha_final))
        
        Vamos detalhar cada parte:
            O primeiro par (coluna_inicial, linha_inicial) indica onde começa a mesclagem
            O segundo par (coluna_final, linha_final) indica onde termina
            (-1) representa a última coluna da tabela

        No meu exemplo específico:
        ('SPAN', (0, 1), (-1, 1))

        Isso significa:
            Começa na primeira coluna (0) da segunda linha (1)
            Termina na última coluna (-1) da segunda linha (1)
            Ou seja, todas as células da segunda linha serão mescladas em uma única célula

        Aqui um exemplo prático:
            from reportlab.platypus import Table
            from reportlab.lib import colors

            data = [
                ['Cabeçalho 1', 'Cabeçalho 2', 'Cabeçalho 3'],
                ['Esta célula ocupará toda a linha'],
                ['Dado 1', 'Dado 2', 'Dado 3']
            ]

            tabela = Table(data)
            tabela.setStyle([
                ('SPAN', (0,1), (-1,1))  # Mescla todas as células da segunda linha
            ])
        """