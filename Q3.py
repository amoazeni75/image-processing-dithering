import cv2
from matplotlib import pyplot as plt
import numpy as np


def draw_histograms(image):
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


def get_heads_color(numbers, level):
    splits_part = []
    split_recersive(splits_part, numbers, level, 0, len(numbers))
    head_colors = []
    for index, item in enumerate(splits_part):
        index_start = 0
        for i in range(0, index):
            index_start += len(splits_part[i])
        avg = get_average(splits_part[index], index_start)
        head_colors.append(avg)
    return head_colors


def split_recersive(splits, numbers, level, index_start, index_end):
    if level == 0:
        splits.append(numbers[index_start:index_end])
        return
    else:
        split_index = get_median_index(numbers[index_start:index_end])
        split_index += index_start
        level -= 1
        split_recersive(splits, numbers, level, index_start, split_index)
        split_recersive(splits, numbers, level, split_index, index_end)


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