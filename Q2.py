from math import floor
from PIL import Image


def dither_matrix():
    w, h = 3, 3
    matrix_original = [[105, 255, 15], [0, 215, 55], [95, 50, 0]]

    for y in range(0, h):
        for x in range(0, w):
            oldpixel = matrix_original[y][x]
            newpixel = apply_threshold_binary(oldpixel)
            matrix_original[y][x] = newpixel
            error = oldpixel - newpixel
            if x < w - 1:
                value_new = matrix_original[y][x + 1] + round(error * 7 / 16)
                matrix_original[y][x + 1] = min(value_new, 255)

            if x > 0 and y < h - 1:
                value_new = matrix_original[y + 1][x - 1] + round(error * 3 / 16)
                matrix_original[y + 1][x - 1] = min(value_new, 255)

            if y < h - 1:
                value_new = matrix_original[y + 1][x] + round(error * 5 / 16)
                matrix_original[y + 1][x] = min(value_new, 255)

            if x < w - 1 and y < h - 1:
                value_new = matrix_original[y + 1][x + 1] + round(error * 1 / 16)
                matrix_original[y + 1][x + 1] = min(value_new, 255)
    print(matrix_original)


def apply_threshold_binary(value):
    return 255 * floor(value /128)


def apply_threshold(value):
    return 85 * floor(value/64)


def floyd_steinberg_dither(image_file):
    """
    https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
    Pseudocode:
    for each y from top to bottom
       for each x from left to right
          oldpixel  := pixel[x][y]
          newpixel  := find_closest_palette_color(oldpixel)
          pixel[x][y]  := newpixel
          quant_error  := oldpixel - newpixel
          pixel[x+1][y  ] := pixel[x+1][y  ] + quant_error * 7/16
          pixel[x-1][y+1] := pixel[x-1][y+1] + quant_error * 3/16
          pixel[x  ][y+1] := pixel[x  ][y+1] + quant_error * 5/16
          pixel[x+1][y+1] := pixel[x+1][y+1] + quant_error * 1/16
    find_closest_palette_color(oldpixel) = floor(oldpixel / 256)
    """

    new_img = Image.open(image_file)

    new_img = new_img.convert('RGB')
    pixel = new_img.load()

    x_lim, y_lim = new_img.size

    for y in range(1, y_lim):
        for x in range(1, x_lim):
            red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

            red_newpixel = apply_threshold(red_oldpixel)
            green_newpixel = apply_threshold(green_oldpixel)
            blue_newpixel = apply_threshold(blue_oldpixel)

            pixel[x, y] = red_newpixel, green_newpixel, blue_newpixel

            red_error = red_oldpixel - red_newpixel
            blue_error = blue_oldpixel - blue_newpixel
            green_error = green_oldpixel - green_newpixel

            if x < x_lim - 1:
                red = pixel[x+1, y][0] + round(red_error * 7/16)
                green = pixel[x+1, y][1] + round(green_error * 7/16)
                blue = pixel[x+1, y][2] + round(blue_error * 7/16)

                pixel[x+1, y] = (red, green, blue)

            if x > 1 and y < y_lim - 1:
                red = pixel[x-1, y+1][0] + round(red_error * 3/16)
                green = pixel[x-1, y+1][1] + round(green_error * 3/16)
                blue = pixel[x-1, y+1][2] + round(blue_error * 3/16)

                pixel[x-1, y+1] = (red, green, blue)

            if y < y_lim - 1:
                red = pixel[x, y+1][0] + round(red_error * 5/16)
                green = pixel[x, y+1][1] + round(green_error * 5/16)
                blue = pixel[x, y+1][2] + round(blue_error * 5/16)

                pixel[x, y+1] = (red, green, blue)

            if x < x_lim - 1 and y < y_lim - 1:
                red = pixel[x+1, y+1][0] + round(red_error * 1/16)
                green = pixel[x+1, y+1][1] + round(green_error * 1/16)
                blue = pixel[x+1, y+1][2] + round(blue_error * 1/16)

                pixel[x+1, y+1] = (red, green, blue)
    new_img.save('../dithered_floyd_steinberg.jpg')


def apply_threshold_orderd(value):
    return floor(value / 64)


def ordered_dithering(image_file):
    matrix_original = [[0, 2], [3, 1]]
    new_img = Image.open(image_file)

    new_img = new_img.convert('RGB')
    pixel = new_img.load()

    x_lim, y_lim = new_img.size

    for y in range(1, y_lim):
        for x in range(1, x_lim):
            red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]

            red_newpixel = apply_threshold_orderd(red_oldpixel)
            green_newpixel = apply_threshold_orderd(green_oldpixel)
            blue_newpixel = apply_threshold_orderd(blue_oldpixel)

            i = x % 2
            j = y % 2
            if red_newpixel > matrix_original[j][i]:
                red_newpixel = 255
            else:
                red_newpixel = 0

            if green_newpixel > matrix_original[j][i]:
                green_newpixel = 255
            else:
                green_newpixel = 0

            if blue_newpixel > matrix_original[j][i]:
                blue_newpixel = 255
            else:
                blue_newpixel = 0

            pixel[x, y] = red_newpixel, green_newpixel, blue_newpixel

    new_img.save('../dithered_ordered.jpg')
