#===============================================================================
# Trabalho 5: ChromaKey
#-------------------------------------------------------------------------------
# Autor: Eduarda Simonis Gavião e Willian Rodrigo Huber
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt

INPUT_IMAGE =  '2.bmp' #carrengando a Imagem com Fundo verde 
BACKGROUND_IMAGE='fundo.jpg' #carregando "fundo" 

def mascara (img):
    rows, cols, _ = img.shape #dimensões da imagem
    mask = np.zeros((rows, cols)) #cria uma imagem zerada com as mesmas dimensões
    
    for i in range(rows): #for para percorrer as linhas
        for j in range(cols): #for para percorrer as colunas
            if img[i, j, 1] > max(img[i, j, 0], img[i, j, 2]): #se o canal G for maior que o máximo B e R 
                mask[i, j] = 1 - max(min((img[i, j, 1] - max(img[i, j, 2], img[i, j, 0])), 255), 0)/255 #faz a máscara em escalas de cinza
            else: 
                mask[i, j] = 1 #caso contrário coloca branco
    
    mask = cv2.normalize(mask, mask, 0, 1, cv2.NORM_MINMAX)  #faz a normalização 
               
    #cv2.imshow("imagem",mask)
    fundo(mask,img) #chamada para remover o fundo verde 
                               
def fundo (mask, img):
    #remover o fundo da imagem original
    rows, cols, _ = img.shape
    
    #tirando o fundo verde da imagem
    for i in range(rows):
        for j in range(cols):
            if mask[i, j] < 0.9:#verifica se a máscara é menor que 0.9, parametros verificando uso nas imagens
                img[i, j] = mask[i, j] #se sim,iguala a imagem com a maascara
    #cv2.imshow("image",img)
    chroma(mask,img) #chamada para adicionar fundo 

def chroma (masked,img):
    #colocando a imagem no fundo 
    fundo = cv2.imread (BACKGROUND_IMAGE)#lê a imagem de fundo
    rows, cols, _ = img.shape #tira as dimensões da imagem 
    saida = np.zeros_like(img) #cria a saída vazia
    fundo = cv2.resize(fundo, (cols, rows)) #redimensiona o fundo para os padrões da imagem
    
    for i in range (rows):#for para linha
        for j in range (cols):#for para coluna
            saida[i,j,[0,1,2]]= img[i,j,[0,1,2]]*min(masked[i,j],1)+ fundo[i,j,[0,1,2]]*(1-masked[i,j]) #saída igual a imagem pelo mínmo da maskara mais o fundo retirando a máscara. 
    

    cv2.imshow("saida",saida)

    
def main ():

    # Abre as imagens 
    img = cv2.imread (INPUT_IMAGE)

    #verifica se pode ser aberta
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()
    
        
        
    mascara(img) #chama a função máscara
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================