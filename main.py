#===============================================================================
# Autores: Eduarda Simonis Gavião (RA: 1879472), Willian Rodrigo Huber(RA: 1992910)
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import cv2
import numpy as np

#===============================================================================

INPUT_IMAGE = 'img/6.bmp'
BACKGROUND_IMAGE = 'fundo.jpg'

#===============================================================================

def main():
    img = cv2.imread(INPUT_IMAGE)
    bg_img = cv2.imread(BACKGROUND_IMAGE)
    rows, cols, _ = img.shape
    bg_img = cv2.resize(bg_img, (cols, rows))
    mask = np.zeros((rows, cols))
    img_out = np.zeros_like(img)

    for i in range(rows):
        for j in range(cols):
            if img[i, j, 1] > max(img[i, j, 0], img[i, j, 2]):
                mask[i, j] = 1 - max(min((img[i, j, 1] - max(img[i, j, 2], img[i, j, 0])), 255), 0)/255
            else:
                mask[i, j] = 1

    mask = cv2.normalize(mask, mask, 0, 1, cv2.NORM_MINMAX)

    for i in range(rows):
        for j in range(cols):
            if mask[i, j] < 1:
                img[i, j, 1] = img[i, j, 2]

    for i in range(rows):
        for j in range(cols):
            img_out[i, j, [0, 1, 2]] = img[i, j, [0, 1, 2]] * min(mask[i, j]*1.1, 1) + bg_img[i, j, [0, 1, 2]] * (1 - mask[i, j])

    #cv2.imshow("Mascara", mask)
    cv2.imshow("Resultado", img_out)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()