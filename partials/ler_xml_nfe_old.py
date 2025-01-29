import xml.etree.ElementTree as ET
from partials.all_imports import *
from querys.local.qry_produto_local import BuscaCodigoProduto

# Inicializa a lista de itens
itens = []

produtos_informatica = {
    '8471': 'Maquinas para processamento de dados...',
    '8443': 'Maquinas e aparelhos por meio de blocos...',
    '8473': 'Partes e acessorios...',
    '8523': 'Discos, fitas, disposit. de armaz de dados...',
    '8517625': 'Aparelhos para transmissão ou recepção de voz...',
    '84145910': 'Microventiladores com área de carcaça inferior a 90 cm2',
    '85043111': 'Transformadores de corrente',
    '85043119': 'Outros transformadores eletr. port < =1KVA, P/ FREQ < =60HZ',
    '85043199': 'Outros transformadores elétricos, potência < =1KVA',
    '85044021': 'Conversores estáticos retificadores, exceto carregadores de acumuladores, de cristal (semicondutores)',
    '85044029': 'Outros conversores estáticos, retificadores, exceto carregadores de acumuladores',
    '85044040': 'Equipamento de alimentação ininterrupta de energia (UPS ou No-Break)',
    '85049010': 'Núcleos de pó ferromagnético',
    '85049090': 'Outras partes de outros transformadores, conversores, etc',
    '85065010': 'Pilhas, baterias eletr. de lítio, vol < =300cm3',
    '85068090': 'Outras pilhas/baterias eletr.',
    '85072010': 'Outros acumuladores elétricos de chumbo, peso < =1000kg',
    '85076000': 'Acumuladores elétricos e seus preparadores mesmo de forma quadrada ou retangular/de íon de lítio',
    '85176213': 'Outros multiplexadores por divisão de tempo',
    '85176234': 'Switch (INCLUSÃO TAX PRÁTICO)',
    '85176241': 'Roteadores wireless',
    '85176248': 'Adaptadores para comunicação com os sitemas de armazenamento de dados',
    '85176251': 'Terminais ou repetidores sobre linhas metálicas',
    '85176252': 'Terminais sobre linhas de fibras ópticas, com velocidade de transmissão superior a 2,5Gbits/s',
    '85176253': 'Terminais de texto que operem com código de V, providos de teclado alfanumérico e visor ("display") mesmo com telefone incorporado',
    '85176254': 'Hub/Switch',
    '85176272': 'Outros aparelhos emissores com receptor incorporado digitais, de frequência inferior a 15 Ghz e de taxa de transmissão inferior ou igual a 34 Mbits/s, exceto os de sistema bidirecional de radiomensagens de taxa de transmissão inferior ou igual a 112 Kbits/s',
    '85176291': 'Aparelhos transmissores',
    '85176294': 'Tradutores (conversores) de protocolos para interconexão de redes (gateways)',
    '85182200': 'Alto-falante (altifalantes) múltiplos montados no seu receptáculo',
    '85182990': 'Alto falantes',
    '85183000': 'Fones de ouvido, mesmo combinados com um microfone, e conjuntos ou sortidos constituídos por um microfone e um ou mais alto-falantes (altifalantes)',
    '85184000': 'Amplificadores elétricos de audiofrequência',
    '85185000': 'Aparelhos elétricos de amplificação de som',
    '85219010': 'Gravador-reprodutor e editor de imagem e som, em discos, por meio magnético, óptico ou optomagnético',
    '85258011': 'Câmeras de televisão com três ou mais captadores de imagem',
    '85258012': 'Câmera com sensor de imagem a semicondutor tipo CCD, de mais de 490 x 580 elementos de imagem (pixels) ativos, sensíveis a intensidades de iluminação inferiores a 0,20 lux.',
    '85258013': 'Câmeras de televisão, outras, próprias para captar imagens exclusivamente no espectro infravermelho de comprimento de onda superior ou igual a 2 micrômetros (mícrons) e inferior ou igual a 14 micrômetros (mícrons)',
    '85258021': 'Câmeras fotográficas digitais e câmeras de vídeo, com três ou mais captadores de imagem',
    '85258022': 'Câmeras fotográficas digitais e câmeras de vídeo, próprias para captar imagens exclusivamente no espectro infravermelho de comprimento de onda superior ou igual a 2 micrômetros (mícrons) e inferior ou igual a 14 micrômetros (mícrons)',
    '85258029': 'Câmera/filmadora digital',
    '85269100': 'GPS',
    '85284220': 'Monitor policromático utilizado por máquinas de processamento de dados',
    '85285220': 'Monitor policromático utilizado por máquinas de processamento de dados',
    '85285920': 'Monitor policromático utilizado por máquinas de processamento de dados',
    '85286200': 'Projetor multimídia utilizado por sistema de processamento de dados',
    '85286910': 'Monitor e projetor com tecnologia digital de microespelhos',
    '85287111': 'Receptor decodificador integrado (IRD) de sinais digitalizados de vídeo codificados',
    '85287119': 'Receptor/decodificador integrado de sinais digitalizados de vídeo codificados',
    '85287190': 'Receptor de TV mesmo que incorpore radiodifusão',
    '85291011': 'Antenas com refletor parabólico, exceto para telefones celulares',
    '85291090': 'Outras antenas e refletores de antenas e suas partes',
    '85366910': 'Tomada polarizada e tomada blindada',
    '85423120': 'Processadores montados, próprios para montagem em superfície (SMD - Surface Mounted Device)',
    '85442000': 'Cabos coaxiais e outros condutores elétricos coaxiais',
    '90011020': 'Feixes e cabos de fibra ópticas',
}

def verifica_existencia_configuracao():
    try:
        # Tente abrir o arquivo JSON para leitura "\\\\server_erp\\alterdat\\db\\chave.key"
        with open('\\\\server_erp\\alterdat\\db\\unificado.json', 'r', encoding='utf-8') as f:
            # Carregue os dados do JSON para o dicionário 'existing_data'
            existing_data = json.load(f) # Mesmo não tendo importação da lib explícita, sabemos que ela existe em all_imports.
        return existing_data
    except FileNotFoundError:
        # Se o arquivo não existir, use o conteúdo inicial definido
        existing_data = unificado_padrao

        # Abra o arquivo JSON para escrita e salve o conteúdo inicial
        with open('\\\\server_erp\\alterdat\\db\\unificado.json', 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        return existing_data

unificado = verifica_existencia_configuracao()

def informatica(ncm):
    if (ncm in produtos_informatica.keys()) or (ncm[0:4] in produtos_informatica.keys()) or (ncm[0:7] in produtos_informatica.keys()):
        return 'S', 'fatores_informatica'
    else:
        return 'N', 'default'

def encontrar_regiao(estado):
    for regiao, estados in unificado["regioes_estados"].items():
        if estado in estados:
            return regiao
    return "Estado não encontrado."

# Dicionário unificado
unificado_padrao = {
    "regioes_estados": {
        "Norte": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
        "Nordeste": ["ES", "AL", "BA", "MA", "PB", "PE", "PI", "RN", "SE"],
        "Ceará": ["CE"],
        "Centro-Oeste": ["DF", "GO", "MT", "MS"],
        "Sudeste": ["MG", "RJ", "SP"],
        "Sul": ["PR", "RS", "SC"]
    },
    "fatores": {
        '35088657000137': {
            'Sul': {
                '1': 22.20, 
                '2': 22.20,
                'default': {'4': 21.20, 'default': 18.20}
            },
            'Sudeste': {
                '1': 22.20, 
                '2': 22.20,
                'default': {'4': 21.20, 'default': 18.20}
            },
            'Norte': {
                '1': 22.54, 
                '2': 22.54,
                'default': {'4': 24.54, '12': 16.54}
            },
            'Nordeste': {
                '1': 22.54, 
                '2': 22.54,
                'default': {'4': 24.54, '12': 16.54}
            },
            'Centro-Oeste': {
                '1': 22.54, 
                '2': 22.54,
                'default': {'4': 24.54, '12': 16.54}
            },
            'Ceará': {
                '1': 9.93, 
                '2': 9.93,
                'default': 6.93
            }
        },
        'default': {
            'Sul': {
                '1': 15.93, 
                '2': 15.93,
                'default': {'4': 13.69, 'default': 11.93}
            },
            'Sudeste': {
                '1': 15.93, 
                '2': 15.93,
                'default': {'4': 13.69, 'default': 11.93}
            },
            'Norte': {
                '1': 16.84, 
                '2': 16.84,
                'default': {'4': 15.54, '12': 10.84}
            },
            'Nordeste': {
                '1': 16.84, 
                '2': 16.84,
                'default': {'4': 15.54, '12': 10.84}
            },
            'Centro-Oeste': {
                '1': 16.84, 
                '2': 16.84,
                'default': {'4': 15.54, '12': 10.84}
            },
            'Ceará': {
                '1': 7.53, 
                '2': 7.53,
                'default': 4.53
            }
        }
    },
    "fatores_informatica": {
        'Sul': {
            '1': 8.33, 
            '2': 8.33,
            'default': {'4': 8.33, 'default': 5.33}
        },
        'Sudeste': {
            '1': 8.33, 
            '2': 8.33,
            'default': {'4': 8.33, 'default': 5.33}
        },
        'Norte': {
            '1': 7.33, 
            '2': 7.33,
            'default': {'4': 13.33, '12': 5.33}
        },
        'Nordeste': {
            '1': 7.33, 
            '2': 7.33,
            'default': {'4': 13.33, '12': 5.33}
        },
        'Centro-Oeste': {
            '1': 7.33, 
            '2': 7.33,
            'default': {'4': 13.33, '12': 5.33}
        },
        'Ceará': {
            '1': 5.11, 
            '2': 5.11,
            'default': 4.11
        }
    },
    "custo": {
        "ir_fat": 13,
        "margem_lucro_esperado": 130,
        "finan": 105
    }
}      

def dicionario_item(posicao, id_produto, quantidade, preco_unitario, ):
    # Cria um dicionário para o item no Faturamento

    return {
    # "Lote": {
    #     "Identificador": "00A0000001",
    #     "Codigo": "01",
    #     "DataFabricacao": data_formatada,
    #     "Observacao": "Observação",
    #     "Perecivel": True,
    #     "DataValidade": data_formatada
    # },
    # "Serie": {
    #     "Identificador": "00A0000001",
    #     "Codigo": "01",
    #     "DataFabricacao": data_formatada,
    #     "Observacao": "Observação",
    #     "SequencialInicial": 123,
    #     "Mascara": "{DIA}"
    # },
    "CFOP": "5.409",
    # "Identificador": posicao, # "00A0000001", # Falta identificar <<<========== A documentação não fala, pediram para não enviar.
    "IdentificadorProduto": id_produto,
    "IdentificadorSetorEntrada": "00A0000001",
    "IdentificadorSetorSaida": "00A000000V",
    # "IdentificadorTipoMovimentoCobranca": "00A0000001",
    "Quantidade": quantidade,
    "ValorUnitario": preco_unitario,
    # "Repasses": [
    #     {
    #     "IdentificadorPessoa": "00A0000001",
    #     "IdentificadorCategoria": "00A0000001",
    #     "AliquotaFaturamento": 10,
    #     "AliquotaDuplicata": 10,
    #     "PossuiRepasseDuplicata": True,
    #     "PossuiRepasseFaturamento": True,
    #     }
    # ]
    }

def formatar_documento(numero):
    if len(numero) == 14:  # CNPJ
        return f"{numero[:2]}.{numero[2:5]}.{numero[5:8]}/{numero[8:12]}-{numero[12:]}"
    elif len(numero) == 11:  # CPF
        return f"{numero[:3]}.{numero[3:6]}.{numero[6:9]}-{numero[9:]}"
    else:
        return "Número inválido"
    # Exemplos de uso:
    # print(formatar_documento("23539810000388"))  # Saída: 23.539.810/0003-88
    # print(formatar_documento("71180672372"))    # Saída: 711.806.723-72

def get_text_or_default(element, tag, namespaces, default=None):
    tag_element = element.find(tag, namespaces)
    return tag_element.text if tag_element is not None else default

def encontrar_valor(data, regiao, icms, crt_emit=None, i=None):
    """
    Encontra o valor no JSON baseado na região, ICMS, CRT e I.
    
    :param data: Dicionário com os dados (carregado do JSON).
    :param regiao: Nome da região (ex: 'Sul').
    :param icms: Valor do ICMS (ex: 4).
    :param crt_emit: Valor do CRT (ex: 1 ou 2).
    :param i: (Opcional) Valor de I (ex: 'S' ou 'N').
    :return: Valor correspondente ou None se não encontrado.
    """
    # Navega até os fatores da região
    fatores = data.get('fatores', {}).get('default', {}).get(regiao, {})
    
    # Caso o ICMS seja 4, verifica diretamente o valor correspondente
    if float(icms) == 4.0:
        if 'default' in fatores and '4' in fatores['default']: # float(icms)
            return fatores['default']['4'] # str(icms)
    
    # Caso o ICMS seja diferente de 4, verifica o valor de ART
    if float(icms) != 4.0 and crt_emit in [1, 2]:
        if str(crt_emit) in fatores:
            return fatores[str(crt_emit)]
    
    # Caso nenhuma condição seja atendida, retorna o valor "default" geral
    if 'default' in fatores and 'default' in fatores['default']:
        return fatores['default']['default']
    
    # Retorna None se nada for encontrado
    return None

def ler_nfe(caminho_arquivo):
    posicao = 1

    # itens = []

    # Definir namespaces usados no XML
    namespaces = {'ns0': 'http://www.portalfiscal.inf.br/nfe'}

    # inicializar dicionário de documento
    nota_fiscal_dict = {}
    # inicializar dicionário de documento
    pessoas_dict = {}
    # Inicializar o dicionário para produtos
    produtos_dict = {}

    # Carregar e parsear o arquivo XML
    try:
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"Erro ao carregar o XML: {e}")

    try:
        # Número da Nota Fiscal
        numero_nota = root.find('.//ns0:ide/ns0:nNF', namespaces)
        numero_nota = numero_nota.text if numero_nota is not None else "Número não encontrado"
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Dados do Emissor
        emit = root.find('.//ns0:emit', namespaces)
        regiao_emit = encontrar_regiao(emit.find('ns0:enderEmit/ns0:UF', namespaces).text if emit.find('ns0:enderEmit/ns0:UF', namespaces) is not None else "Endereço não encontrado")
        crt_emit = emit.find('ns0:CRT', namespaces).text if emit.find('ns0:CRT', namespaces) is not None else "CRT não encontrado"
        # ***** CRT significa *****
        # 1: Simples Nacional
        # 2: Simples Nacional - Excesso de Sublimite de Receita Bruta
        # 3: Regime Normal
        # 4: Microempreendedor Individual (MEI) - Novo código, implementado a partir de setembro de 2024
        # Criar dicionário do emissor
        emissor = {
            'nome': emit.find('ns0:xNome', namespaces).text if emit.find('ns0:xNome', namespaces) is not None else "Emitente não encontrado",
            'cnpj': emit.find('ns0:CNPJ', namespaces).text if emit.find('ns0:CNPJ', namespaces) is not None else "CNPJ não encontrado",
            'endereco': emit.find('ns0:enderEmit/ns0:xLgr', namespaces).text if emit.find('ns0:enderEmit/ns0:xLgr', namespaces) is not None else "Endereço não encontrado",
            'regiao': regiao_emit,
            'crt': crt_emit,
        }
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Dados do Cliente
        dest = root.find('.//ns0:dest', namespaces)
        # Criar dicionário de destinatário
        destinatario = {
            'nome':  dest.find('ns0:xNome', namespaces).text if dest.find('ns0:xNome', namespaces) is not None else "Destinatário não encontrado",
            'cnpj_cpf': dest.find('ns0:CNPJ', namespaces).text if dest.find('ns0:CNPJ', namespaces) is not None else "CNPJ não encontrado",
            'endereco': dest.find('ns0:enderDest/ns0:xLgr', namespaces).text if dest.find('ns0:enderDest/ns0:xLgr', namespaces) is not None else "Endereço não encontrado",
            
        }

        # Formata o CNPJ ou CPF das pessoas da nota
        cpf_cnpj_fornecedor = formatar_documento(emissor['cnpj'])  # Formatar o CNPJ do emissor
        emissor['cnpj'] = cpf_cnpj_fornecedor

        cpf_cnpj_destinatario = formatar_documento(destinatario['cnpj_cpf'])  # Formatar o CNPJ do emissor
        destinatario['cnpj_cpf'] = cpf_cnpj_destinatario        
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Dados do documento
        total = root.find('.//ns0:total', namespaces)
        # Cria dicionário de totais
        totais = {
            'frete': total.find('ns0:ICMSTot/ns0:vFrete', namespaces).text if total.find('ns0:ICMSTot/ns0:vFrete', namespaces) is not None else 0,
            'frete_manual': 0,
            'valor_produtos' : total.find('ns0:ICMSTot/ns0:vProd', namespaces).text if total.find('ns0:ICMSTot/ns0:vProd', namespaces) is not None else 0,
            'ir_fat': 13,
        }
        # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Inicializar posição com valor 1
        posicao = 1
        # Produtos
        for det in root.findall('.//ns0:det', namespaces):
            prod = det.find('ns0:prod', namespaces)
            imposto = det.find('ns0:imposto', namespaces)

            codigo_produto_fornecedor = prod.find('ns0:cProd', namespaces).text if prod.find('ns0:cProd', namespaces) is not None else "Código não encontrado"

            # Buscar informações adicionais do produto
            if codigo_produto_fornecedor.isdigit():
                print("O código contém apenas números.")
                codigo_produto_fornecedor = codigo_produto_fornecedor.zfill(6)
            else:
                print("O código contém caracteres não numéricos.")
                
            qry_produto_local = BuscaCodigoProduto(codigo_produto_fornecedor, emissor['cnpj'])
            dicionario_produto_fornecedor = qry_produto_local.get_all_produtos_filtered()

            def verificar_produto(dicionario_produto_fornecedor, codigo_produto_fornecedor, event_bus):
                if not dicionario_produto_fornecedor:
                    error_message = f"Produto com código {codigo_produto_fornecedor.zfill(6)} não encontrado. Provavelmente não está vinculado ao CNPJ deste fornecedor."
                    event_bus.send("error_occurred", error_message)  # Envia uma mensagem de erro
                    return

            if not dicionario_produto_fornecedor:
                return codigo_produto_fornecedor #.zfill(6) < Zeros à esquerda
                # raise ValueError(f"Produto com código {codigo_produto_fornecedor.zfill(6)} não encontrado. Provavelmente não está vinculado ao CNPJ deste fornecedor.")

            # Adicionar produto ao dicionário principal
            id_produto = dicionario_produto_fornecedor['IdProduto']  # Chave principal
            ncm = prod.find('ns0:NCM', namespaces).text if prod.find('ns0:NCM', namespaces) is not None else "NCM não encontrado"
            is_informatica, tipo_produto = informatica(ncm)
           
            # Criar dicionário do produto
            produto = {
                'IdProduto': id_produto,
                'codigo': dicionario_produto_fornecedor['CodigoProdutoBimer'], # A
                'CodigoProdutoFornecedor': prod.find('ns0:cProd', namespaces).text if prod.find('ns0:cProd', namespaces) is not None else "Código não encontrado",
                'descricao': dicionario_produto_fornecedor['NmProduto'],
                'quantidade': prod.find('ns0:qCom', namespaces).text if prod.find('ns0:qCom', namespaces) is not None else "Quantidade não encontrada",
                'valor_unitario': prod.find('ns0:vUnCom', namespaces).text if prod.find('ns0:vUnCom', namespaces) is not None else 0, # C
                'valor_total': prod.find('ns0:vProd', namespaces).text if prod.find('ns0:vProd', namespaces) is not None else "Valor total não encontrado",
                'valor_frete': prod.find('ns0:vFrete', namespaces).text if prod.find('ns0:vFrete', namespaces) is not None else 0, # G
                'desconto_item': prod.find('ns0:vDesc', namespaces).text if prod.find('ns0:vDesc', namespaces) is not None else 0, # G
                'p_frete': 0,
                'ncm': ncm,
                'i': is_informatica,
                'fator': tipo_produto,
                # -------------------------------------------------------------------------------------------
                'PrecoVendaAnterior': dicionario_produto_fornecedor['PrecoVendaAnterior'],
                'MediaFreteCalculado': (float(0) + float(totais['frete'])) / float(totais['valor_produtos']),
                'Custos': 0,
                'MargemLucroAtual': 0,
                'MargemLucroEsperado': 130,
                'Finan': 105,
                'impostos': {}
            }

            # Adicionar impostos ao dicionário do produto
            # ICMS
            icms00 = imposto.find('.//ns0:ICMS/ns0:ICMS00', namespaces)
            if icms00 is not None:
                icms_item = icms00.find('ns0:pICMS', namespaces).text if icms00.find('ns0:pICMS', namespaces) is not None else "Alíquota não encontrada"
                produto['impostos']['ICMS'] = {
                    'origem': icms00.find('ns0:orig', namespaces).text if icms00.find('ns0:orig', namespaces) is not None else "Origem não encontrada",
                    'CST': icms00.find('ns0:CST', namespaces).text if icms00.find('ns0:CST', namespaces) is not None else "CST não encontrado",
                    'modalidade_base_calculo': icms00.find('ns0:modBC', namespaces).text if icms00.find('ns0:modBC', namespaces) is not None else "Modalidade não encontrada",
                    'base_calculo': icms00.find('ns0:vBC', namespaces).text if icms00.find('ns0:vBC', namespaces) is not None else "Base cálculo não encontrada",
                    'aliquota': icms_item,
                    'aliquota_calculada': encontrar_valor(unificado, regiao_emit, icms_item, crt_emit), # E
                    'valor': icms00.find('ns0:vICMS', namespaces).text if icms00.find('ns0:vICMS', namespaces) is not None else "Valor ICMS não encontrado"
                }
            # else:
            #     produto['impostos']['ICMS'] = {
            #         'origem': 0,
            #         'CST': '99',
            #         'modalidade_base_calculo': 3,
            #         'base_calculo': 0,
            #         'aliquota': 0,
            #         'aliquota_calculada': 0, # D
            #         'valor': 0
            #     }  
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            icms20 = imposto.find('.//ns0:ICMS/ns0:ICMS20', namespaces)
            # print(f'======>> {icms20}')
            if icms20 is not None:
                icms_item = icms20.find('ns0:pICMS', namespaces).text if icms20.find('ns0:pICMS', namespaces) is not None else "Alíquota não encontrada"
                produto['impostos']['ICMS'] = {
                    'origem': icms20.find('ns0:orig', namespaces).text if icms20.find('ns0:orig', namespaces) is not None else "Origem não encontrada",
                    'CST': icms20.find('ns0:CST', namespaces).text if icms20.find('ns0:CST', namespaces) is not None else "CST não encontrado",
                    'modalidade_base_calculo': icms20.find('ns0:modBC', namespaces).text if icms20.find('ns0:modBC', namespaces) is not None else "Modalidade não encontrada",
                    'base_calculo': icms20.find('ns0:vBC', namespaces).text if icms20.find('ns0:vBC', namespaces) is not None else "Base cálculo não encontrada",
                    'aliquota': icms_item,
                    'aliquota_calculada': 20-float(icms_item), # D
                    'valor': icms20.find('ns0:vICMS', namespaces).text if icms20.find('ns0:vICMS', namespaces) is not None else "Valor ICMS não encontrado"
                }
            # else:
            #     produto['impostos']['ICMS'] = {
            #         'origem': 0,
            #         'CST': '99',
            #         'modalidade_base_calculo': 3,
            #         'base_calculo': 0,
            #         'aliquota': 0,
            #         'aliquota_calculada': 0, # D
            #         'valor': 0
            #     }                
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            icms30 = imposto.find('.//ns0:ICMS/ns0:ICMS30', namespaces)
            # print(f'======>> {icms20}')
            if icms30 is not None:
                icms_item = icms30.find('ns0:pICMSST', namespaces).text if icms30.find('ns0:pICMSST', namespaces) is not None else "Alíquota não encontrada"
                produto['impostos']['ICMS'] = {
                    'origem': icms30.find('ns0:orig', namespaces).text if icms30.find('ns0:orig', namespaces) is not None else "Origem não encontrada",
                    'CST': icms30.find('ns0:CST', namespaces).text if icms30.find('ns0:CST', namespaces) is not None else "CST não encontrado",
                    'modalidade_base_calculo': icms30.find('ns0:modBCST', namespaces).text if icms30.find('ns0:modBCST', namespaces) is not None else "Modalidade não encontrada",
                    'base_calculo': icms30.find('ns0:vBCST', namespaces).text if icms30.find('ns0:vBCST', namespaces) is not None else "Base cálculo não encontrada",
                    'aliquota': icms_item,
                    'aliquota_calculada': 20-float(icms_item), # D
                    'valor': icms30.find('ns0:vICMSST', namespaces).text if icms30.find('ns0:vICMSST', namespaces) is not None else "Valor ICMS não encontrado"
                }
            # else:
            #     produto['impostos']['ICMS'] = {
            #         'origem': 0,
            #         'CST': '99',
            #         'modalidade_base_calculo': 3,
            #         'base_calculo': 0,
            #         'aliquota': 0,
            #         'aliquota_calculada': 0, # D
            #         'valor': 0
            #     }                
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------            
            # IPI
            ipi = imposto.find('.//ns0:IPI/ns0:IPITrib', namespaces)
            if ipi is not None:
                produto['impostos']['IPI'] = {
                    'CST': ipi.find('ns0:CST', namespaces).text if ipi.find('ns0:CST', namespaces) is not None else "CST não encontrado",
                    'vBC': ipi.find('ns0:vBC', namespaces).text if ipi.find('ns0:vBC', namespaces) is not None else "Valor IPI não encontrado",
                    'pIPI': ipi.find('ns0:pIPI', namespaces).text if ipi.find('ns0:pIPI', namespaces) is not None else 0, # D
                    'vIPI': ipi.find('ns0:vIPI', namespaces).text if ipi.find('ns0:vIPI', namespaces) is not None else "Valor IPI não encontrado"
                }
            else:
                produto['impostos']['IPI'] = {
                    'CST': '99',
                    'vBC': 0,
                    'pIPI': 0,
                    'vIPI': 0
                }                
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # PIS
            pis = imposto.find('.//ns0:PIS/ns0:PISAliq', namespaces)
            if pis is not None:
                produto['impostos']['PIS'] = {
                    'CST': pis.find('ns0:CST', namespaces).text if pis.find('ns0:CST', namespaces) is not None else "CST não encontrado",
                    'base_calculo': pis.find('ns0:vBC', namespaces).text if pis.find('ns0:vBC', namespaces) is not None else "Base cálculo não encontrada",
                    'aliquota': pis.find('ns0:pPIS', namespaces).text if pis.find('ns0:pPIS', namespaces) is not None else "Alíquota não encontrada",
                    'valor': pis.find('ns0:vPIS', namespaces).text if pis.find('ns0:vPIS', namespaces) is not None else "Valor PIS não encontrado"
                }
            else:
                produto['impostos']['PIS'] = {
                    'CST': '99',
                    'base_calculo': 0,
                    'aliquota': 0,
                    'valor': 0
                }                
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # COFINS
            cofins = imposto.find('.//ns0:COFINS/ns0:COFINSAliq', namespaces)
            if cofins is not None:
                produto['impostos']['COFINS'] = {
                    'CST': cofins.find('ns0:CST', namespaces).text if cofins.find('ns0:CST', namespaces) is not None else "CST não encontrado",
                    'base_calculo': cofins.find('ns0:vBC', namespaces).text if cofins.find('ns0:vBC', namespaces) is not None else "Base cálculo não encontrada",
                    'aliquota': cofins.find('ns0:pCOFINS', namespaces).text if cofins.find('ns0:pCOFINS', namespaces) is not None else "Alíquota não encontrada",
                    'valor': cofins.find('ns0:vCOFINS', namespaces).text if cofins.find('ns0:vCOFINS', namespaces) is not None else "Valor COFINS não encontrado"
                }
            else:
                produto['impostos']['COFINS'] = {
                    'CST': 0,
                    'base_calculo': 0,
                    'aliquota': 0,
                    'valor': 0,
                }
            # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            produto['p_frete'] = (float(totais['frete']) / float(totais['valor_produtos'])) * 100  # 100 Pode ser transformado em percentual aqui?
            produto['Custos'] = float(produto['impostos']['IPI']['pIPI']) + float(produto['impostos']['ICMS']['aliquota_calculada']) + float(unificado["custo"]["ir_fat"]) + float(produto['p_frete']) + 100 # 100 Pode ser transformado em percentual aqui?
            produto['MargemLucroAtual'] = float(produto['PrecoVendaAnterior'] * 100) / (float(produto['valor_unitario']) * (float(produto['Custos'])/100) * (float(unificado["custo"]["ir_fat"])/100)) # 100 Pode ser transformado em percentual aqui?
            produto['PrecoVendaCalculado'] = (float(produto['valor_unitario']) * (float(produto['Custos'])/100) * (float(unificado["custo"]["margem_lucro_esperado"])/100) * (float(unificado["custo"]["finan"])/100)) # 100 Pode ser transformado em percentual aqui?

            # Adicionar o produto ao dicionário usando o IdProduto como chave
            produtos_dict[id_produto] = produto
            # print(json.dumps(produto, indent=4))
            item = dicionario_item(posicao, produto['IdProduto'], float(produto['quantidade']), float(produto['valor_unitario']))
            itens.append(item)
            posicao += 1
        
        nota = {
            'numero_nota': numero_nota,
            'emissor': emissor,
            'destinatario': destinatario,
            'produtos': produtos_dict,
            'totais': totais
        }
        print(json.dumps(nota, indent=4))
        return nota
    except Exception as e:
        # raise ValueError(f"Produto com código {codigo_produto_fornecedor.zfill(6)} não encontrado. Provavelmente não está vinculado ao CNPJ deste fornecedor.")
        raise ValueError(f"Erro ao processar a NFE: {e}")
