import cv2


def convert_gray_bin(raw_image):
    image_gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    (thresh, image_binary) = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow('Original image', raw_image)
    cv2.imshow('Gray image', image_gray)
    cv2.imshow('Binary image', image_binary)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
