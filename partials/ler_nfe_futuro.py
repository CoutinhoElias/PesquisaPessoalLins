# 1. SEPARAÇÃO DE RESPONSABILIDADES
from partials.all_imports import *
from querys.local.qry_produto_local import BuscaCodigoProduto

# Classe para lidar com XML
class NFEXMLHandler:
    def __init__(self):
        self.namespaces = {'ns0': 'http://www.portalfiscal.inf.br/nfe'}
    
    def get_element_text(self, element, path, default=None):
        """Método utilitário para extrair texto de elementos XML"""
        found = element.find(path, self.namespaces)
        return found.text if found is not None else default
    
    def parse_emissor(self, emit_element):
        """Extrai informações do emissor do XML"""
        return {
            'nome': self.get_element_text(emit_element, 'ns0:xNome', "Emitente não encontrado"),
            'cnpj': self.get_element_text(emit_element, 'ns0:CNPJ', "CNPJ não encontrado"),
            'endereco': self.get_element_text(emit_element, 'ns0:enderEmit/ns0:xLgr', "Endereço não encontrado"),
            'uf': self.get_element_text(emit_element, 'ns0:enderEmit/ns0:UF', "UF não encontrada"),
            'crt': self.get_element_text(emit_element, 'ns0:CRT', "CRT não encontrado")
        }
    
    def parse_produto(self, prod_element):
        """Extrai informações do produto do XML"""
        return {
            'codigo': self.get_element_text(prod_element, 'ns0:cProd'),
            'ncm': self.get_element_text(prod_element, 'ns0:NCM'),
            'quantidade': self.get_element_text(prod_element, 'ns0:qCom'),
            'valor_unitario': self.get_element_text(prod_element, 'ns0:vUnCom'),
            'valor_total': self.get_element_text(prod_element, 'ns0:vProd'),
            'valor_frete': self.get_element_text(prod_element, 'ns0:vFrete', '0'),
            'desconto': self.get_element_text(prod_element, 'ns0:vDesc', '0')
        }

# Classe para processamento de impostos
class ImpostoProcessor:
    def __init__(self, xml_handler):
        self.xml_handler = xml_handler
    
    def process_icms(self, imposto_element):
        """Processa informações de ICMS"""
        icms_tags = ['ICMS00', 'ICMS20', 'ICMS30']
        
        for tag in icms_tags:
            icms = imposto_element.find(f'.//ns0:ICMS/ns0:{tag}', self.xml_handler.namespaces)
            if icms is not None:
                return self._extract_icms_info(icms, tag)
        
        return self._get_default_icms()
    
    def _extract_icms_info(self, icms_element, icms_type):
        """Extrai informações específicas do ICMS baseado no tipo"""
        if icms_type == 'ICMS00':
            aliquota = self.xml_handler.get_element_text(icms_element, 'ns0:pICMS', '0')
            base_calc = 'ns0:vBC'
            valor = 'ns0:vICMS'
        elif icms_type == 'ICMS20':
            aliquota = self.xml_handler.get_element_text(icms_element, 'ns0:pICMS', '0')
            base_calc = 'ns0:vBC'
            valor = 'ns0:vICMS'
        else:  # ICMS30
            aliquota = self.xml_handler.get_element_text(icms_element, 'ns0:pICMSST', '0')
            base_calc = 'ns0:vBCST'
            valor = 'ns0:vICMSST'
            
        return {
            'origem': self.xml_handler.get_element_text(icms_element, 'ns0:orig', '0'),
            'CST': self.xml_handler.get_element_text(icms_element, 'ns0:CST', '99'),
            'base_calculo': self.xml_handler.get_element_text(icms_element, base_calc, '0'),
            'aliquota': aliquota,
            'valor': self.xml_handler.get_element_text(icms_element, valor, '0')
        }

# 2. TRATAMENTO DE ERROS

class NFEError(Exception):
    """Classe base para exceções relacionadas à NFE"""
    pass

class XMLParseError(NFEError):
    """Erro ao fazer parse do XML"""
    pass

class ProdutoError(NFEError):
    """Erro relacionado a produtos"""
    pass

class ImpostoError(NFEError):
    """Erro relacionado a impostos"""
    pass

# Classe principal refatorada
class LerNFE:
    def __init__(self):
        self.xml_handler = NFEXMLHandler()
        self.imposto_processor = ImpostoProcessor(self.xml_handler)
        self.itens = []
    
    def ler_nfe(self, caminho_arquivo):
        try:
            tree = ET.parse(caminho_arquivo)
            root = tree.getroot()
        except ET.ParseError as e:
            raise XMLParseError(f"Erro ao fazer parse do XML: {str(e)}")
        except FileNotFoundError:
            raise XMLParseError(f"Arquivo não encontrado: {caminho_arquivo}")
        
        try:
            # Processamento do XML
            emissor = self.xml_handler.parse_emissor(root.find('.//ns0:emit', self.xml_handler.namespaces))
            
            for det in root.findall('.//ns0:det', self.xml_handler.namespaces):
                try:
                    self._process_item(det, emissor)
                except ProdutoError as e:
                    # Log do erro e continue processando outros itens
                    logging.error(f"Erro ao processar produto: {str(e)}")
                    continue
                
        except Exception as e:
            raise NFEError(f"Erro geral ao processar NFE: {str(e)}")
    
    def _process_item(self, det, emissor):
        try:
            prod = det.find('ns0:prod', self.xml_handler.namespaces)
            imposto = det.find('ns0:imposto', self.xml_handler.namespaces)
            
            if prod is None:
                raise ProdutoError("Elemento produto não encontrado no XML")
                
            produto_info = self.xml_handler.parse_produto(prod)
            
            # Validação do código do produto
            if not produto_info['codigo']:
                raise ProdutoError("Código do produto não encontrado")
                
            # Processamento de impostos
            try:
                impostos = {
                    'ICMS': self.imposto_processor.process_icms(imposto)
                }
                produto_info['impostos'] = impostos
                
            except ImpostoError as e:
                logging.warning(f"Erro ao processar impostos: {str(e)}")
                produto_info['impostos'] = self._get_default_impostos()
            
            self.itens.append(self._create_item(produto_info))
            
        except Exception as e:
            raise ProdutoError(f"Erro ao processar item: {str(e)}")
            
    def _get_default_impostos(self):
        """Retorna estrutura padrão de impostos para casos de erro"""
        return {
            'ICMS': {
                'origem': '0',
                'CST': '99',
                'base_calculo': '0',
                'aliquota': '0',
                'valor': '0'
            }
        }