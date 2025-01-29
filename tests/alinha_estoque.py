# pip install pyautogui pillow mouseinfo
# from mouseinfo import mouseInfo
# mouseInfo()
# pyinstaller --onefile --add-data ".\assets;assets" --hidden-import pymssql .\main.py


import pyautogui
import time
import sys
import os
import json
import pygetwindow as gw

from datetime import datetime, timedelta

# Obter a data atual
data_atual = datetime.now()

# email = None
# password = None

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from partials.find_images import ImageFinder

def verifica_existencia_configuracao():
    try:
        # Tente abrir o arquivo JSON para leitura
        with open('cfg_robo.json', 'r', encoding='utf-8') as f:
            # Carregue os dados do JSON para o dicionário 'existing_data'
            existing_data = json.load(f)

        email = existing_data["username"]
        password = existing_data["password"]
        return email, password

    except FileNotFoundError:
        # Se o arquivo não existir, use o conteúdo inicial definido
        email.value = None
        password.value = None


email, password = verifica_existencia_configuracao()

# Caminhos das imagens dos campos
usuario_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\usuario_bimer.png"
senha_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\senha_bimer.png"  
caminho_botao = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_avancar2.png"
icone_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\icone_bimer.png"
botao_logar = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_logar.png"
grupo_configurador = r"C:\Users\elias\Documents\PesquisaPessoal\assets\grupo_configurador.png"
aba_financeiro = r"C:\Users\elias\Documents\PesquisaPessoal\assets\aba_financeiro.png"
aba_estoque = r"C:\Users\elias\Documents\PesquisaPessoal\assets\aba_estoque.png"
menu_alinhamentos = r"C:\Users\elias\Documents\PesquisaPessoal\assets\menu_alinhamentos.png"
menu_alinhamento_estoque = r"C:\Users\elias\Documents\PesquisaPessoal\assets\menu_alinhamento_estoque.png"
botao_avancar = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_avancar.png"
botao_avancar2 = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_avancar2.png"
botao_adicionar = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_adicionar.png"
botao_escolhe_empresa_1 = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_escolhe_empresa_1.png"
botao_adicionar_todos = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_adicionar_todos.png"
campo_data_inicial = r"C:\Users\elias\Documents\PesquisaPessoal\assets\campo_data_inicial.png"
botao_concluir = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_concluir.png"
botao_fechar = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_fechar.png"
botao_fechar_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_fechar_bimer.png"
botao_fechar_sistema = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_fechar_sistema.png"

# Criando uma instância
finder = ImageFinder(confidence=0.9)

# Minimizo dodas as janelas
pyautogui.hotkey('win', 'd') 

# ------------------------------------------------------------------------------------
# Procurando uma imagem do atalho para abrir o Bimer
coords = finder.find_image(icone_bimer)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.doubleClick()
# ------------------------------------------------------------------------------------
# Procurando uma imagem do campo de usuário Bimer
coords = finder.find_image(usuario_bimer)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.doubleClick()
    pyautogui.typewrite(email)
# ------------------------------------------------------------------------------------
# Procurando uma imagem do campo de senha Bimer
coords = finder.find_image(senha_bimer)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click()
    pyautogui.typewrite(password)
    pyautogui.click(x,y+110, duration=1) # Clicando no botão.
# ------------------------------------------------------------------------------------
# Procurando uma imagem do menu que abre o configurador.
coords = finder.find_image(grupo_configurador)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click()
    pyautogui.click(x,y+30, duration=1) # Clicando no botão.
# ------------------------------------------------------------------------------------
# Procurando uma imagem ABA ESTOQUE
coords = finder.find_image(aba_estoque)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click(x, y)
# ------------------------------------------------------------------------------------
# Procurando uma imagem ABA ALINHAMENTOS
coords = finder.find_image(menu_alinhamentos)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click(x, y)
    pyautogui.click(x,y+100, duration=1) # Clicando no botão.


# ------------------------------------------------------------------------------------
# Procurando uma imagem BOTAO AVANÇAR
coords = finder.find_image(botao_avancar)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click(x, y)
    # pyautogui.click(x,y+100, duration=1) # Clicando no botão.

# ------------------------------------------------------------------------------------
# Procurando uma imagem BOTAO AVANÇAR
coords = finder.find_image(botao_adicionar)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click(x, y)
    # pyautogui.click(x,y+100, duration=1) # Clicando no botão.

# ------------------------------------------------------------------------------------
# Procurando uma imagem BOTAO AVANÇAR
coords = finder.find_image(botao_escolhe_empresa_1)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.doubleClick(x, y)
    # pyautogui.click(x,y+100, duration=1) # Clicando no botão.

# ------------------------------------------------------------------------------------
# Procurando uma imagem BOTAO AVANÇAR
time.sleep(2)
pyautogui.hotkey('alt', 'n') # Avancar

# coords = finder.find_image(botao_avancar2)
# if coords:
#     x, y = coords
#     pyautogui.moveTo(x, y)  # Move o mouse para a posição
#     pyautogui.click(x, y)

# ------------------------------------------------------------------------------------
# Procurando uma imagem BOTAO AVANÇAR
coords = finder.find_image(botao_adicionar_todos)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click(x, y)

# ------------------------------------------------------------------------------------
time.sleep(2)
pyautogui.hotkey('alt', 'n') # Avançar depois de adicionar a empresa 1
pyautogui.hotkey('alt', 'n') # Avançar novamente pois não faz nada nesta tela.

# Procurando uma imagem BOTAO AVANÇAR
# coords = finder.find_image(botao_avancar2)
# if coords:
#     x, y = coords
#     pyautogui.moveTo(x, y)  # Move o mouse para a posição
#     pyautogui.click(x, y)
#     pyautogui.click(x, y)

# Subtrair 2 dias da data atual
data_2_dias_atras = data_atual - timedelta(days=2)

# Formatar a data para exibição (opcional)
data_formatada = data_2_dias_atras.strftime('%dd/%md/%YYYY')

# Mostrar a data de 2 dias anteriores
print("Data de 2 dias atrás:", data_formatada)

# ------------------------------------------------------------------------------------
# Procurando uma imagem do campo de usuário Bimer
coords = finder.find_image(campo_data_inicial) # Preenche a data
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.doubleClick()
    pyautogui.typewrite(data_formatada)

time.sleep(2)
pyautogui.hotkey('alt', 'o') # Pressiona em Concluir para iniciar

time.sleep(60)
pyautogui.hotkey('alt', 'f') # Fecha o formulário de alinhamento

# ------------------------------------------------------------------------------------
# Procurando uma imagem do campo de usuário Bimer
coords = finder.find_image(botao_fechar_bimer)
if coords:
    x, y = coords
    pyautogui.moveTo(x, y)  # Move o mouse para a posição
    pyautogui.click()

# ------------------------------------------------------------------------------------
# Procurando uma imagem do campo de usuário Bimer
# coords = finder.find_image(botao_fechar_sistema)
# if coords:
#     x, y = coords
#     pyautogui.moveTo(x, y)  # Move o mouse para a posição
#     pyautogui.click()

time.sleep(2)
pyautogui.hotkey('alt', 'f') # Fecha o formulário de alinhamento









# ------------------------------------------------------------------------------------------------------------------------------
# import pyautogui
# import time
# import os

# procurar = "SIM"
# usuario_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\senha_bimer.png"

# # Verifica se o arquivo existe
# if not os.path.exists(usuario_bimer):
#     print(f"O caminho da imagem está incorreto ou a imagem não existe: {usuario_bimer}")
#     print(f"Caminho absoluto: {os.path.abspath(usuario_bimer)}")
#     exit()

# while procurar == "SIM":
#     try:
#         imagem = pyautogui.locateOnScreen(usuario_bimer, confidence=0.8)
        
#         if imagem:
#             # Calcula o centro da imagem para clicar
#             x = imagem.left + (imagem.width / 2)
#             y = imagem.top + (imagem.height / 2)
            
#             pyautogui.click(x, y)
#             print(f"Imagem encontrada em: {x}, {y}")
#             procurar = "NÃO"
        
#     except Exception as e:
#         print(f"Erro ao procurar imagem: {str(e)}")
#         time.sleep(1)
#         print("Imagem não encontrada")
# ------------------------------------------------------------------------------------------------------------------------------

# import pyautogui
# import time
# import os
# # from partials.find_images import ImageFinder
# import sys
# import os
# # Adiciona o diretório raiz ao path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from partials.find_images import ImageFinder


# # usuario_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\senha_bimer.png"

# # Caminhos das imagens dos campos
# usuario_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\usuario_bimer.png"
# senha_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\senha_bimer.png"  
# caminho_botao = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_avancar2.png"
# icone_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\icone_bimer.png"


# # Criar instância do ImageFinder
# finder = ImageFinder(usuario_bimer)

# # Apenas encontrar as coordenadas
# coordinates = finder.find_image()
# if coordinates:
#     print(f"Imagem encontrada em: x={coordinates.x}, y={coordinates.y}")
# else:
#     print("Imagem não encontrada")

# # Ou encontrar e clicar automaticamente
# # Com limite máximo de 5 tentativas
# if finder.find_and_double_click(max_attempts=5):
#     print("Imagem encontrada e clicada com sucesso!")
# else:
#     print("Não foi possível encontrar a imagem após 5 tentativas")


# ------------------------------------------------------------------------------------------------------------------------------



# def focus_window(window_title):
#     try:
#         windows = gw.getWindowsWithTitle(window_title)
#         if windows:
#             app_window = windows[0]
#             app_window.activate()  # Ativa a janela
#             time.sleep(0.5)  # Tempo para garantir o foco
#             print(f"Janela '{window_title}' ativada com sucesso!")
#             return True
#         else:
#             print(f"Janela '{window_title}' não encontrada!")
#             return False
#     except Exception as e:
#         print(f"Erro ao ativar a janela: {e}")
#         return False

# def find_and_clear_field(image_path, max_attempts=5, window_title="bimer"):
#     """
#     Garante que o campo correto seja encontrado e limpo, com foco forçado na janela.
#     """
#     # try:
#     #     # Focar na janela correta
#     #     windows = gw.getWindowsWithTitle(window_title)
#     #     if windows:
#     #         app_window = windows[0]
#     #         app_window.activate()
#     #         print(f"Janela '{window_title}' ativada.")
#     #         time.sleep(1)  # Garantir que o foco seja ativado
#     #     else:
#     #         print(f"Janela '{window_title}' não encontrada.")
#     #         return False
#     # except Exception as e:
#     #     print(f"Erro ao ativar a janela: {e}")
#     #     return False

#     # Criar instância do ImageFinder
#     finder = ImageFinder(image_path)

#     # Tentar encontrar a imagem
#     # coordinates = finder.find_image(max_attempts)
#     coordinates = finder.find_and_double_click(max_attempts)

#     if coordinates:
#         print(f"Campo encontrado em: x={coordinates.x}, y={coordinates.y}")
        
#         # Mover o mouse para a posição exata do campo
#         # pyautogui.moveTo(coordinates.x, coordinates.y, duration=0.5)elias frotaelias frota      time.sleep(0.5)

#         # Garantir o foco no local com duplo clique
#         print("Executando duplo clique no ponto encontrado...")
#         pyautogui.doubleClick()
#         time.sleep(0.5)

#         # Pressionar Delete para limpar o conteúdo do campo
#         print("Limpando o campo...")
#         pyautogui.press('delete')
#         pyautogui.typewrite('elias frota')

#         print("Conteúdo do campo apagado com sucesso!")
#         return True
#     else:
#         print(f"Não foi possível encontrar o campo após {max_attempts} tentativas")
#         return False


# # Usar a função
# if __name__ == "__main__":
#     # Configurar um pequeno delay para cada comando do PyAutoGUI
#     pyautogui.PAUSE = 0.1

#     # Encontrar a janela do aplicativo (substitua o nome da janela com o título correto do aplicativo)
#     window = gw.getWindowsWithTitle('Bimer')[0]

#     # Ativar a janela para garantir que ela esteja em foco
#     window.activate()
    
#     # Tenta encontrar e limpar o campo de usuário
#     find_and_clear_field(usuario_bimer)

# ------------------------------------------------------------------------------------------------------------------------------
# def minimizar_tudo():
#     # Minimizo dodas as janelas
#     pyautogui.hotkey('win', 'd')    

# def clicar_avancar(caminho_imagem_botao):
#     """
#     Localiza e clica no botão Avançar usando uma imagem limpa
#     """
#     print("=== Iniciando busca pelo botão Avançar ===")
#     pyautogui.PAUSE = 1.0  # Pausa entre ações
    
#     if not os.path.exists(caminho_imagem_botao):
#         print("O caminho da imagem está incorreto ou a imagem não existe.")
#         return False

#     try:
#         # Primeira tentativa - busca exata
#         print("Procurando botão na tela...")
#         Botao_Avançar = pyautogui.locateOnScreen(caminho_imagem_botao, confidence=0.8)  # Usando confidence
        
#         # Se não encontrar, tenta com grayscale
#         if not Botao_Avançar:
#             print("Tentando busca em escala de cinza...")
#             Botao_Avançar = pyautogui.locateCenterOnScreen(caminho_imagem_botao, grayscale=True)
        
#         if Botao_Avançar:
#             centro = pyautogui.center(Botao_Avançar)
#             print(f"Botão encontrado em: {centro}")
            
#             # Move o mouse e clica
#             pyautogui.moveTo(centro.x, centro.y, duration=0.5)
#             time.sleep(0.2)
#             pyautogui.click()
#             print("Clique realizado com sucesso!")
#             return True
#         else:
#             print("\nBotão não encontrado. Verifique se:")
#             print("1. A janela está visível e ativa")
#             print("2. O botão 'Avançar' está visível")
#             print("3. Não há outras janelas sobrepondo")
#             return False
            
#     except Exception as e:
#         print(f"Erro durante a operação: {str(e)}")
#         return False

# def abre_bimer(caminho_imagem_icone):
    
#     """
#     Localiza e clica no botão Avançar usando uma imagem limpa
#     """
#     print("=== Iniciando busca pelo botão Avançar ===")
#     pyautogui.PAUSE = 1.0  # Pausa entre ações
    
#     if not os.path.exists(caminho_imagem_icone):
#         print("O caminho da imagem está incorreto ou a imagem não existe.")
#         return False

#     try:
#         # Primeira tentativa - busca exata
#         print("Procurando botão na tela...")
#         icone_bimer = pyautogui.locateOnScreen(caminho_imagem_icone, confidence=0.8)  # Usando confidence
        
#         # Se não encontrar, tenta com grayscale
#         if not icone_bimer:
#             print("Tentando busca em escala de cinza...")
#             icone_bimer = pyautogui.locateCenterOnScreen(caminho_imagem_icone, grayscale=True)
        
#         if icone_bimer:
#             centro = pyautogui.center(icone_bimer)
#             print(f"Botão encontrado em: {centro}")
            
#             # Move o mouse e clica
#             pyautogui.moveTo(centro.x, centro.y, duration=0.5)
#             time.sleep(0.2)
#             pyautogui.doubleClick()
#             print("Clique realizado com sucesso!")
#             return True
#         else:
#             print("\nBotão não encontrado. Verifique se:")
#             print("1. A janela está visível e ativa")
#             print("2. O botão 'Avançar' está visível")
#             print("3. Não há outras janelas sobrepondo")
#             return False
            
#     except Exception as e:
#         print(f"Erro durante a operação: {str(e)}")
#         return False  

# def preencher_campo(imagem_campo, texto):
#     """
#     Localiza um campo na tela usando uma imagem e insere texto nele.
#     """
#     print(f"=== Buscando o campo para preencher com: '{texto}' ===")

#     procurar = "SIM"

#     if not os.path.exists(imagem_campo):
#         print(f"Erro: O caminho da imagem {imagem_campo} está incorreto ou a imagem não existe.")
#         return False

#     try:
#         campo = None
#         # Tentativas de localizar a imagem
#         for tentativa in range(3):
#             print(f"Tentativa {tentativa + 1} de localizar o campo '{imagem_campo}'...")
#             campo = pyautogui.locateOnScreen(imagem_campo, confidence=0.8)

#             if not campo:
#                 print("Tentando com escala de cinza...")
#                 campo = pyautogui.locateOnScreen(imagem_campo, confidence=0.8, grayscale=True)

#             if campo:
#                 break
#             print("Campo não encontrado. Tentando novamente...")
#             time.sleep(1)

#         if campo is None:
#             print(f"Erro: Não foi possível localizar o campo '{imagem_campo}'. Verifique a imagem e a tela.")
#             return False

#         x, y = pyautogui.center(campo)
#         print(f"Campo enusuariousuariocontrado em: ({x}, {y})")

#         # Movendo e preenchendo o campo
#         pyautogui.moveTo(x, y, duration=0.5)
#         pyautogui.doubleClick()
#         time.sleep(0.5)
#         pyautogui.typewrite(texto)
#         print(f"Texto '{texto}' inserido com sucesso!")
#         return True

#     except Exception as e:
#         print(f"Erro ao preencher o campo: {str(e)}")
#         return False


# if __name__ == "__main__":
#     # Caminhos das imagens dos campos
#     usuario_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\usuario_bimer.png"
#     senha_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\senha_bimer.png"  

#     caminho_botao = r"C:\Users\elias\Documents\PesquisaPessoal\assets\botao_avancar2.png"
#     icone_bimer = r"C:\Users\elias\Documents\PesquisaPessoal\assets\icone_bimer.png"


#     # Preenche o campo do usuário
#     sucesso_usuario = preencher_campo(usuario_bimer, "ELIAS FROTA")
    
#     minimizar_tudo()
#     abre_bimer(icone_bimer)

#     # Preenche o campo do usuário
#     sucesso_usuario = preencher_campo(usuario_bimer, "ELIAS FROTA")
    
#     # Se o campo de usuário foi preenchido com sucesso, tenta o campo de senha
#     if sucesso_usuario:
#         preencher_campo(senha_bimer, "123456")

    
        


    # clicar_avancar(caminho_botao)





# MINIMIZAR TUDO

# ABRIR BIMER

# ABRIR CONFIGURADOR

# ADICIONAR FILTROS

# RODAR

# import os

# import pandas as pd
# from pandas import to_datetime

# import locale

# pyautogui.press('backspace')

# pyautogui.click(493,552, duration=1)
# pyautogui.click(1366,280, duration=1)
# pyautogui.click(749,281, duration=1)

# pyautogui.hotkey('alt', 's')
# pyautogui.hotkey('alt', 'n')
# pyautogui.hotkey('alt', 'p')

# pyautogui.click(1156,291, duration=1)

# pyautogui.typewrite(row['Código'])
# pyautogui.hotkey('alt', 'l')
# pyautogui.hotkey('alt', 'o')

# pyautogui.hotkey('alt', 't')

# pyautogui.move(0, duration=2)

# # pyautogui.moveTo(1399,329, duration=2)
# for i in range(0, 10):
#     # pyautogui.typewrite(valor_formatado)
#     # Pressione a tecla de seta para baixo
#     pyautogui.keyDown('down')

# pyautogui.hotkey('alt', 'r')
# pyautogui.hotkey('alt', 's')
# pyautogui.hotkey('alt', 'f')  

    #-------------------------------------------------------------------------------------------------
    # Vincular produto com empresa.

    # pyautogui.click(779,371 )
    # pyautogui.move(779,371, duration=1)
    # pyautogui.typewrite(row['Código'])
    # pyautogui.press('enter')
    # pyautogui.hotkey('alt', 'o')
    # pyautogui.press('space')
    # print(row['Código'], ' - ',row['Nome do produto'])


# import pyautogui
# import time
# import PySimpleGUI as sg
# import pandas as pd
# from pandas import to_datetime
# import locale
# import pytesseract
# from PIL import Image

# # Configuração do pytesseract para o Windows
# # Ajuste o caminho se você tiver instalado o Tesseract em um local diferente
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# # Definir a localização como "Português do Brasil"
# locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# # Layout da janela
# layout = [
#     [sg.Text('Caminho do arquivo Excel')],
#     [sg.Input(key='-CAMINHO-'), sg.FileBrowse(file_types=(("Excel Files", "*.xlsx"),))],
#     [sg.Button('OK', disabled=False), sg.Button('Cancel')]
# ]

# # Criar a janela
# janela = sg.Window('Ajuste de Margem por planilha.', layout)

# # Função para apagar espaços
# def apaga_espacos():
#     for i in range(100):
#         pyautogui.press('backspace')

# # Função para capturar uma região específica da tela e fazer OCR
# def encontra_codigo_na_tela(codigo_procurado, region):
#     screenshot = pyautogui.screenshot(region=region)
#     texto = pytesseract.image_to_string(screenshot)
#     return codigo_procurado in texto

# while True:
#     evento, valores = janela.read()

#     if evento == sg.WIN_CLOSED or evento == 'Cancel':
#         break
#     caminho_arquivo = valores['-CAMINHO-']

#     # Carregar dados do Excel
#     df_itens_planilha = pd.read_excel(caminho_arquivo, dtype={'Código': str})
#     df_itens_planilha['Código'] = df_itens_planilha['Código'].fillna(0)
#     df_itens_planilha['Código'] = df_itens_planilha['Código'].astype(str).str.zfill(6)

#     if evento == 'OK':
#         for _, row in df_itens_planilha.iterrows():
#             codigo = row['Código']
#             vl_reposicao = float(format(row['Reposicao'], '.2f'))
#             valor_formatado = locale.currency(vl_reposicao)
#             print(f'{codigo} - {row["Nome do produto"]} - {valor_formatado}')

#             # Defina a região onde o código é exibido na tela (ajuste os valores conforme necessário)
#             region = (500, 300, 400, 200)  # x, y, largura, altura

#             # Tente encontrar o código específico na tela com OCR
#             encontrado = False
#             for _ in range(5):  # Tenta rolar a tela algumas vezes para procurar o código
#                 if encontra_codigo_na_tela(codigo, region):
#                     encontrado = True
#                     break
#                 else:
#                     pyautogui.scroll(-500)  # Rola a tela para baixo se o código não foi encontrado

#             # Se o código foi encontrado, clique na posição
#             if encontrado:
#                 # Posicione o clique no ponto onde o código foi detectado (ajuste a posição conforme necessário)
#                 pyautogui.click(region[0] + 10, region[1] + 10, duration=1)
                
#                 # Ações após encontrar o produto correto
#                 pyautogui.click(493, 552, duration=1)
#                 pyautogui.click(1366, 280, duration=1)
#                 pyautogui.click(749, 281, duration=1)
                
#                 pyautogui.hotkey('alt', 's')
#                 pyautogui.hotkey('alt', 'n')
#                 pyautogui.hotkey('alt', 'p')

#                 pyautogui.click(1156, 291, duration=3)
#                 pyautogui.typewrite(codigo)
#                 pyautogui.hotkey('alt', 'l')
#                 pyautogui.hotkey('alt', 'o')
#                 pyautogui.hotkey('alt', 't')

#                 # Digitar o valor formatado
#                 for _ in range(10):
#                     pyautogui.typewrite(valor_formatado)
#                     pyautogui.keyDown('down')

#                 pyautogui.hotkey('alt', 'r')
#                 pyautogui.hotkey('alt', 's')
#                 pyautogui.hotkey('alt', 'f')
#             else:
#                 print(f"Código {codigo} não encontrado na tela.")

#         pyautogui.scroll(500)  # Restaura a posição inicial da tela

# janela.close()
