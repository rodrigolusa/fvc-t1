import cv2
import numpy as np
from math import log10, sqrt

#Função que captura o clique na imagem
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
      if(len(p) < 4):                 # Aceita somente os 4 primeiros cliques
        p.append([x,y])               # Insere o ponto clicado no array
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, '(' + str(x) + ',' + str(y) + ')', (x+5,y-5), font, 0.4, (255, 0, 0), 1)
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1) 
        cv2.imshow('Imagem', img)

#Função para calculo quantitativo
def PSNR(img_origin, img_result):
    mse = np.mean((img_origin - img_result) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

if __name__=="__main__":
    
    #Informar o nome da imagem de input
    img_name = 'img/foto1_cap1.jpg'
    img_result_name = 'img/foto2_gt.jpg'

    #Leitura das imagens
    img = cv2.imread(img_name, 1)
    img2 = cv2.imread(img_name, 1)
    img_result = cv2.imread(img_result_name, 1)

    #Identifica se a imagem está em retrato ou paisagem
    if(img.shape[0] > img.shape[1]):
      isPortrait = True
    else:
      isPortrait = False

    #Informar o tamanho desejado da imagem
    img_width = 1024
    img_height = 768

    #Ajuste do tamanho
    if isPortrait:
      img_size = (img_height, img_width)
    else:
      img_size = (img_width, img_height)

    #Ajusta tamanho da imagem
    img = cv2.resize(img, img_size)
    img2 = cv2.resize(img, img_size)
    img_result = cv2.resize(img_result, img_size)

    #Array com coordenadas do quatro cantos
    p =[]
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "Ordem dos cliques na foto:", (20,20), font, 0.7, (255, 0, 0), 2)
    cv2.putText(img, "Superior ESQ -> Superior DIR -> Inferior DIR -> Inferior ESQ -> ENTER", (20,40), font, 0.5, (255, 0, 0), 1)
    #Solicitação para clicar nos quatro cantos
    cv2.imshow('Imagem', img)
    cv2.setMouseCallback('Imagem', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #Arrays necessários para a homografia
    pts_src = np.array(p)
    pts_dst = np.array([[0, 0],[img2.shape[1], 0],[img2.shape[1], img2.shape[0]],[0, img2.shape[0]]])

    #Execução da homografia e correção de perspectiva
    h, status = cv2.findHomography(pts_src, pts_dst)
    im_out = cv2.warpPerspective(img2, h, (img2.shape[1],img2.shape[0]))

    #Exibição do resultado e gravação da imagem de saída
    cv2.imwrite('output.jpg', im_out)
    cv2.imshow('Imagem Resultado', im_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    result = PSNR(img_result, im_out)
    print("PSNR: " + str(result))

    print("--- > Concluido! <---")