from math import floor


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