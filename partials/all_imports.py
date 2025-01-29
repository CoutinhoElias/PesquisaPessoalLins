# from configs.settings import USER, PASSWORD, HOST, DATABASE, connection_string

import flet as ft
import pandas as pd
# from pandas import to_datetime
from datetime import datetime
data = datetime.now()
data_formatada = data.strftime('%Y-%m-%d 00:00:00.000')

import json
from urllib.parse import quote
import os
import shutil
import glob
import requests

import subprocess
import platform

import openpyxl
from openpyxl.styles import PatternFill
import xmltodict

# Definir a localização como "Português do Brasil"
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

from datetime import datetime

from configs.settings import Criptografia
from configs.alterdata_api_config import BimerAPIParams
from configs.alterdata_api_base_connection import BaseConnection
from database.users_firebase import FirebaseAuth
from database.models import Pessoa, PessoaCategoria, PedidoDeCompra, PedidoDeCompraItem, LoteDoc, LoteDocItem, ControleAlcadaRegra, Codigo, Produto, CodigoProduto, Unidade, vwProdutoFornecedor, PedidoDeVendaItem

from sqlalchemy import create_engine, text, Column, update, insert, select, and_, distinct, func, case
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

from partials.data_table_person import create_datatable, my_table, sort_column

import xml.etree.ElementTree as ET
import logging

from partials.button import MyButton
from partials.region_tile import region_tile
from partials.region_tile import (fields_norte, fields_ceara, fields_sul, fields_centro_oeste, fields_sudeste)
# from partials.ler_nfe import *

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# CRIPTOGRAFA
# 0 - Instancio a classe de criptografar senhas
criptografia = Criptografia()
# 1 - Chamo a função de criação da chave
criptografia.init_criptografia()

# Conecta a máquina para consultar minhas queries.
engine = create_engine(criptografia.get_senha_descriptografada())

# Criar uma sessão
Session = sessionmaker(bind=engine)
# session = Session()


# Função para formatar a data atual
def format_current_date():
    data = datetime.now()
    return data.strftime('%Y-%m-%d 00:00:00.000')

# Data formatada
data_formatada = format_current_date()

