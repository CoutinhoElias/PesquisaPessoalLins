# import pyautogui
# import time
# from typing import Optional, Tuple

# class ImageFinder:
#     def __init__(self, confidence: float = 0.8):
#         """
#         Inicializa o ImageFinder com um nível de confiança para a busca de imagens.
        
#         Args:
#             confidence (float): Nível de confiança para matching de imagens (0 a 1)
#         """
#         self.confidence = confidence
#         pyautogui.PAUSE = 1  # Adiciona pausa de 1 segundo entre comandos
#         self.max_attempts = 20  # Número máximo de tentativas

#     def find_image(self, image_path: str) -> Optional[Tuple[int, int]]:
#         """
#         Procura uma imagem na tela e retorna suas coordenadas.
#         Tenta encontrar a imagem até 20 vezes, com intervalo de 1 segundo entre tentativas.
        
#         Args:
#             image_path (str): Caminho para o arquivo de imagem
            
#         Returns:
#             Optional[Tuple[int, int]]: Coordenadas (x, y) da imagem ou None se não encontrada
#         """
#         attempts = 0
        
#         while attempts < self.max_attempts:
#             try:
#                 print(f"Tentativa {attempts + 1} de {self.max_attempts} para encontrar a imagem...")
#                 location = pyautogui.locateCenterOnScreen(
#                     image_path,
#                     confidence=self.confidence
#                 )
                
#                 if location:
#                     print(f"Imagem encontrada na posição {location}")
#                     return location
                    
#             except Exception as e:
#                 print(f"Erro ao procurar imagem {image_path}: {str(e)}")
            
#             attempts += 1
#             if attempts < self.max_attempts:
#                 print("Imagem não encontrada. Aguardando 1 segundo para nova tentativa...")
#                 time.sleep(1)
            
#         print(f"Imagem não encontrada após {self.max_attempts} tentativas: {image_path}")
#         return None

import pyautogui
import time
from typing import Optional, Tuple

class ImageFinder:
    def __init__(self, confidence: float = 0.8):
        """
        Inicializa o ImageFinder com um nível de confiança para a busca de imagens.
        
        Args:
            confidence (float): Nível de confiança para matching de imagens (0 a 1)
        """
        self.confidence = confidence
        pyautogui.PAUSE = 1  # Adiciona pausa de 1 segundo entre comandos

    def find_image(self, image_path: str, timeout: Optional[int] = None) -> Optional[Tuple[int, int]]:
        """
        Procura uma imagem na tela e retorna suas coordenadas.
        Continua procurando indefinidamente até encontrar a imagem, com intervalo de 1 segundo entre tentativas.
        
        Args:
            image_path (str): Caminho para o arquivo de imagem
            timeout (Optional[int]): Tempo máximo em segundos para procurar a imagem. 
                                   Se None, procura indefinidamente.
            
        Returns:
            Optional[Tuple[int, int]]: Coordenadas (x, y) da imagem ou None se atingir o timeout
        """
        attempts = 0
        start_time = time.time()
        
        while True:
            try:
                attempts += 1
                print(f"Tentativa {attempts} para encontrar a imagem...")
                
                location = pyautogui.locateCenterOnScreen(
                    image_path,
                    confidence=self.confidence
                )
                
                if location:
                    print(f"Imagem encontrada na posição {location}")
                    return location
                    
            except Exception as e:
                print(f"Erro ao procurar imagem {image_path}: {str(e)}")
            
            if timeout and (time.time() - start_time) > timeout:
                print(f"Tempo limite de {timeout} segundos atingido. Imagem não encontrada: {image_path}")
                return None
                
            print("Imagem não encontrada. Aguardando 1 segundo para nova tentativa...")
            time.sleep(1)