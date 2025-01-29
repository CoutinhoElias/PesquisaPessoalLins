
def dicionario_item(item, posicao):
    # Cria um dicionário para o item
    item = {
        "Acrescimo": {
            "Tipo": "A",
            "Aliquota": 0,
            "Valor": 0
        },
        "CFOP": "5.102",
        "COFINS": {
            "CodigoSituacaoTributaria": "01"
        },
        "Desconto": {
            "Tipo": "A",
            "Aliquota": 0,
            "Valor": 0
        },
        "Frete": {
            "Tipo": "D",
            "Valor": 0
        },
        "ICMS": {
            "CodigoSituacaoTributaria": "00"
        },
        "OrigemProduto": 0,
        "Outros": {
            "ValorSeguro": 0,
            "ValorOutrasDespesas": 0
        },
        "PIS": {
            "CodigoSituacaoTributaria": "01"
        },
        "Repasses": [
            {
                "AliquotaComissao": 0,
                "AliquotaComissaoDuplicata": 0,
                "AliquotaComissaoFaturamento": 0,
                "IdentificadorCategoria": "000000000R",
                "IdentificadorPessoa": "00A00005WH",
                "PossuiRepasseDuplicata": True,
                "PossuiRepasseFaturamento": True,
                "Principal": True
            }
        ],
        "Status": "L",
        "Posicao": posicao,  # Atribui a posição
        # Aplica as transformações nos campos conforme especificado
        "IdentificadorProduto": id_produto,
        "QuantidadePedida": round(quantidade, 2),
        "Valor": round(round(preco_unitario, 2) * round(quantidade, 2), 2), # preco_unitario * row['Transferir'],
        "ValorUnitario": round(preco_unitario, 2) # preco_unitario
    }

    # Incrementa a posição para o próximo item
    posicao += 1

    # Adiciona o dicionário à lista de itens
    itens.append(item)