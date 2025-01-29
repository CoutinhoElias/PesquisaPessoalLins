import os
import json
import pymssql
# import pyodbc
from cryptography.fernet import Fernet

# USER = os.getenv('DB_USER', 'sa')
# PASSWORD = os.getenv('DB_PASSWORD', 'Abc*123')
# HOST = os.getenv('DB_HOST', '192.168.254.1')
# DATABASE = os.getenv('DB_NAME', 'ALTERDATA')

# # Configuração da conexão
# connection_string = f'mssql+pymssql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'

# # String de conexão
# connection_string_odbc = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     f'SERVER={HOST};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
# )

# -------------------------------------------------------------------------------------------------------------------------------------------

class Criptografia:
    def __init__(self):
        self.chave_arquivo = "\\\\server_erp\\alterdat\\db\\chave.key"
        self.senha_arquivo = "cfg_sql.json"

    def gerar_chave(self):
        chave = Fernet.generate_key()
        with open(self.chave_arquivo, "wb") as chave_arquivo:
            chave_arquivo.write(chave)

    def carregar_chave(self):
        return open(self.chave_arquivo, "rb").read()

    def criptografar_senha(self, senha):
        chave = self.carregar_chave()
        fernet = Fernet(chave)
        senha_criptografada = fernet.encrypt(senha.encode())
        return senha_criptografada

    def descriptografar_senha(self, senha_criptografada):
        chave = self.carregar_chave()
        fernet = Fernet(chave)
        senha_descriptografada = fernet.decrypt(senha_criptografada).decode()
        return senha_descriptografada

    def salvar_senha_criptografada(self, senha_criptografada):
        with open(self.senha_arquivo, "w") as json_file:
            json.dump({"senha": senha_criptografada.decode()}, json_file)

    def carregar_senha_criptografada(self):
        with open(self.senha_arquivo, "r") as json_file:
            dados = json.load(json_file)
            # return dados["password"].encode()
            return dados

    def init_criptografia(self):
        if not os.path.exists(self.chave_arquivo):
            self.gerar_chave()

    def get_senha_descriptografada(self):
        self.init_criptografia()
        json_carregado = self.carregar_senha_criptografada()
        # senha_carregada = self.carregar_senha_criptografada()
        senha_descriptografada = self.descriptografar_senha(json_carregado['password'].encode())
        _sa = json_carregado['user']
        _password = senha_descriptografada
        _host = json_carregado['host']
        _database = json_carregado['database']

        # conection_descriptografado = {
        #     "user": _sa,
        #     "password": _password,
        #     "host": _host,
        #     "database": _database
        # }

        connection_string = f'mssql+pymssql://{_sa}:{_password}@{_host}/{_database}'
        return connection_string

# Exemplo de uso
# criptografia = Criptografia()

# # Solicitar a senha do usuário e criptografá-la
# senha_usuario = input("Digite a senha do banco de dados: ") # VALOR DO CAMPO NO MODAL
# senha_criptografada = criptografia.criptografar_senha(senha_usuario)
# criptografia.salvar_senha_criptografada(senha_criptografada)

# # Quando precisar acessar o banco de dados
# senha_descriptografada = criptografia.get_senha_descriptografada()
# print(f"Senha descriptografada: {senha_descriptografada}")