import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image


def draw_histograms(image, image_file):
    histogram_red = cv2.calcHist([image], [0], None, [256], [0, 256])
    histogram_green = cv2.calcHist([image], [1], None, [256], [0, 256])
    histogram_blue = cv2.calcHist([image], [2], None, [256], [0, 256])

    plt.plot(histogram_red, color='red')
    plt.plot(histogram_green, color='green')
    plt.plot(histogram_blue, color='blue')
    plt.legend(('Red', 'Green', 'Blue'), loc='upper right')
    plt.show()

    red_heads = get_heads_color(histogram_red, 3)
    green_heads = get_heads_color(histogram_green, 3)
    blue_heads = get_heads_color(histogram_blue, 2)

    reduce_colors(red_heads, green_heads, blue_heads, image_file)


def get_heads_color(numbers, level):
    splits_part = []
    split_recursive(splits_part, numbers, level, 0, len(numbers))
    head_colors = []
    for index, item in enumerate(splits_part):
        index_start = 0
        for i in range(0, index):
            index_start += len(splits_part[i])
        avg = get_average(splits_part[index], index_start)
        head_colors.append(avg)
    return head_colors


def split_recursive(splits, numbers, level, index_start, index_end):
    if level == 0:
        splits.append(numbers[index_start:index_end])
        return
    else:
        split_index = get_median_index(numbers[index_start:index_end])
        split_index += index_start
        level -= 1
        split_recursive(splits, numbers, level, index_start, split_index)
        split_recursive(splits, numbers, level, split_index, index_end)


def get_median_index(numbers):
    differences = []
    for i in range(1, len(numbers)):
        left = np.sum(numbers[0:i])
        right = np.sum(numbers[i:len(numbers)])
        differences.append(abs(left - right))
    min_index = differences.index(min(differences))
    return min_index


def get_average(numbers, start_index):
    sum = 0
    sum_freq = 0
    for index, freq in enumerate(numbers):
        sum += freq*(index + start_index)
        sum_freq += freq
    return int(sum/sum_freq)


def reduce_colors(red_heads, green_heads, blue_heads, image_input):
    new_img = Image.open(image_input)
    new_img = new_img.convert('RGB')
    pixel = new_img.load()

    x_lim, y_lim = new_img.size

    for y in range(1, y_lim):
        for x in range(1, x_lim):
            red_oldpixel, green_oldpixel, blue_oldpixel = pixel[x, y]
            red_newpixel = find_nearest_value(red_heads, red_oldpixel)
            green_newpixel = find_nearest_value(green_heads, green_oldpixel)
            blue_newpixel = find_nearest_value(blue_heads, blue_oldpixel)
            pixel[x, y] = red_newpixel, green_newpixel, blue_newpixel

    new_img.save('../Median_color_reduced.jpg')


def find_nearest_value(palette, color):
    min_err = abs(palette[0] - color)
    best_choice = palette[0]
    for i in range(1, len(palette)):
        new_err = abs(palette[i] - color)
        if new_err < min_err:
            min_err = new_err
            best_choice = palette[i]
    return best_choice
