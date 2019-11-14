# -*- coding: utf-8 -*-
"""
@author: S.Alirzea Moazeni, 9423110
Multimedia HW2
Dithering
"""
import cv2
import Q1
import Q2
import Q3


def main():
    image_raw = cv2.imread('../cheetah-640x480.jpg')
    # Q1.convert_gray_bin(image_raw)
    # Q2.dither_matrix()
    Q3.floyd_steinberg_dither('../cheetah-640x480.jpg')


if __name__ == '__main__':
    main()