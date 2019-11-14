# -*- coding: utf-8 -*-
"""
@author: S.Alirzea Moazeni, 9423110
Multimedia HW2
Dithering
"""
import cv2
import Q1


def main():
    image_raw = cv2.imread('../cheetah-640x480.jpg')
    Q1.convert_gray_bin(image_raw)


if __name__ == '__main__':
    main()